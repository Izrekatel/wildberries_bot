from telegram import InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from constants import callback_data, commands, keyboards, messages, states
from handlers.menu import menu_callback
from services import wh_ratio


async def rate_callback(update, context):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.RATE_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON)
    )
    return states.RATE_RESULT


async def rate_result_callback(update, context):
    """Функция-вывод результата Отслеживание коэффициента приемки WB"""
    parser_result = await wh_ratio.full_search(update.message.text)
    result = await prepare_answer(parser_result)
    if result is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.UNKNOWN_COMMAND_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result,
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
        )
    return states.END


async def prepare_answer(parser_result):
    answer = f'Коэффицианты приемки:\nМонопаллет: {parser_result.get("Монопаллет")}\nСуперсейф: {parser_result.get("Суперсейф")}\nКороб: {parser_result.get("Короб")}\n'
    return answer


async def cancel_rate_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context, message=messages.CANCEL_MESSAGE)
    return states.END


rate_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            rate_callback,
            pattern=callback_data.GET_RATE
        )],
        states={states.RATE_RESULT: [MessageHandler(filters.TEXT,
                                                    rate_result_callback)]},
        fallbacks=[
            CallbackQueryHandler(
                cancel_rate_callback,
                pattern=callback_data.CANCEL_RATE
            ),
            CommandHandler(commands.MENU, menu_callback),
            CommandHandler(commands.START, menu_callback),
        ],
        allow_reentry=True
    )


def rate_handlers(app):
    app.add_handler(rate_conv)
