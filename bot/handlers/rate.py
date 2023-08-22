from telegram import InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from constants import callback_data, constant, keyboards, messages, states
from handlers import menu
from services import aio_client, wh_ratio


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
    return await rate_callback(
        update, context, text=messages.INCORRECT_STORE_INPUT_MESSAGE
    )


async def rate_result_callback(update, context):
    """Функция-вывод результата Отслеживание коэффициента приемки WB."""
    parser_result = await wh_ratio.full_search(int(update.message.text))
    user_data = {
        "warehouse_id": update.message.text,
        "user_id": update.effective_user.id,
    }
    if not parser_result:
        parser_result = messages.NO_STORE_MESSAGE.format(update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=parser_result,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )
    await rate_request_to_db(user_data)
    return states.END


async def rate_request_to_db(user_data: dict) -> None:
    """Добавление запроса оэффициента приемки WB к БД."""
    await aio_client.post(constant.REQUEST_RATE_URL, data=user_data)


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
        CallbackQueryHandler(menu.cancel, pattern=callback_data.CANCEL),
    ],
    allow_reentry=True,
)


def rate_handlers(app: Application) -> None:
    app.add_handler(rate_conv)
