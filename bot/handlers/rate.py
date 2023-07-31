from telegram import InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from constants import callback_data, keyboards, messages, states
from handlers import menu
from services import wh_ratio


async def rate_callback(update, context, text=messages.RATE_MESSAGE):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON),
    )
    return states.RATE_RESULT


async def rate_incorrent_callback(update, context):
    """Функция-обработчик для некорректного ввода номера склада."""
    await rate_callback(
        update, context, text=messages.INCORRECT_STORE_INPUT_MESSAGE
    )


async def rate_result_callback(update, context):
    """Функция-вывод результата Отслеживание коэффициента приемки WB."""
    parser_result = await wh_ratio.full_search(int(update.message.text))
    if not parser_result:
        parser_result = messages.NO_STORE_MESSAGE.format(update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=parser_result,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
    )
    return states.END


rate_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(rate_callback, pattern=callback_data.GET_RATE)
    ],
    states={
        states.RATE_RESULT: [
            MessageHandler(filters.Regex(r"^\d+$"), rate_result_callback),
            MessageHandler(filters.TEXT, rate_incorrent_callback),
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


def rate_handlers(app):
    app.add_handler(rate_conv)
