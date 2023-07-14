from telegram import InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from constants import (
    callback_data, commands, keyboards, messages, states, constant)
from handlers.menu import menu_callback
from services import aio_client, stock


async def stock_callback(update, context):
    """Функция-обработчик для кнопки Парсер остатков."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.STOCK_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON)
    )
    return states.STOCK_RESULT


async def stock_result_callback(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    parser_result = await stock.stock_parser(article=update.message.text)
    result = await prepare_result(parser_result)
    user_data = {
        "articul": update.message.text
    }
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
    )
    await aio_client.post(constant.REQUEST_STOCK_URL, user_data)
    return states.END


async def prepare_result(parser_result):
    answer = 'Результат:\nОстатки по складам\n\n'
    if parser_result:
        for elem in parser_result:
            size = elem.get('Название')
            whs = elem.get('Склады')
            if size:
                answer += f'Размеры {size}:\n'
            for wh in whs:
                id = wh.get('ID Склада')
                ammount = wh.get('Количество')
                answer += f'{constant.WAREHOUSES.get(id)}: {ammount} шт.\n'
            answer += '\n'
    else:
        answer += 'отсуствуют.'
    return answer


async def cancel_stock_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context, message=messages.CANCEL_MESSAGE)
    return states.END


stock_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            stock_callback,
            pattern=callback_data.GET_STOCK
        )],
        states={states.STOCK_RESULT: [MessageHandler(filters.Regex(r'^\d+$'),
                                                     stock_result_callback)]},
        fallbacks=[
            CallbackQueryHandler(
                cancel_stock_callback,
                pattern=callback_data.CANCEL_STOCK
            ),
            CommandHandler(commands.MENU, menu_callback),
            CommandHandler(commands.START, menu_callback),
        ],
        allow_reentry=True
    )


def stock_handlers(app):
    app.add_handler(stock_conv)
