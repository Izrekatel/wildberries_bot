from telegram import InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from constants import callback_data, constant, keyboards, messages, states
from handlers import menu
from services import aio_client, stock


async def stock_callback(update, context):
    """Функция-обработчик для кнопки Парсер остатков."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.STOCK_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON),
    )
    return states.STOCK_RESULT


async def stock_result_callback(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    parser_result = await stock.stock_parser(article=update.message.text)
    result = await prepare_result(parser_result)
    user_data = {"articul": update.message.text}
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
    )
    await aio_client.post(constant.REQUEST_STOCK_URL, user_data)
    return states.END


async def prepare_result(parser_result):
    answer = "Результат:\nОстатки по складам\n\n"
    if parser_result:
        for elem in parser_result:
            size = elem.get("Название")
            whs = elem.get("Склады")
            if size:
                answer += f"Размеры {size}:\n"
            for wh in whs:
                id = wh.get("ID Склада")
                ammount = wh.get("Количество")
                answer += f"{constant.WAREHOUSES.get(id)}: {ammount} шт.\n"
            answer += "\n"
    else:
        answer += "отсуствуют."
    return answer


async def cancel_stock_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu.menu_callback(update, context)
    return states.END


stock_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(stock_callback, pattern=callback_data.GET_STOCK)
    ],
    states={
        states.STOCK_RESULT: [
            MessageHandler(filters.Regex(r"^\d+$"), stock_result_callback)
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.cancel_callback, pattern=callback_data.CANCEL
        ),
        CallbackQueryHandler(menu.menu_callback, pattern=callback_data.MENU),
    ],
    allow_reentry=True,
)


def stock_handlers(app):
    app.add_handler(stock_conv)
