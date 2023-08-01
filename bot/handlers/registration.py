from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from config import BOT_URL, CHAT_ID
from constants import callback_data, constant, keyboards, messages
from handlers import menu
from services import aio_client


async def start_callback(update, context):
    """Функция-обработчик для команды /start."""
    chat = update.effective_chat
    await context.bot.send_message(
        chat_id=chat.id,
        text=messages.START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.START_KEYBOARD),
    )


async def check_subscribe(update) -> bool:
    """Функция-проверки подписки пользователя на целевой канал."""
    data = {"chat_id": f"{CHAT_ID}", "user_id": f"{update.effective_user.id}"}
    subscribe = await aio_client.get(BOT_URL, data)
    return subscribe["result"]["status"] == "member"


async def subscription_callback(update, context):
    """Функция-проверки и внесения в БД нового подписчика."""
    if await check_subscribe(update):
        await aio_client.post(
            url=constant.REQUEST_TELEGRAM_USER_URL,
            data={"user_id": f"{update.effective_user.id}"},
        )
        return await menu.menu(update, context, message=messages.HELLO_MESSAGE)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=messages.FALSE_SUBSCRIBE_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.START_KEYBOARD),
    )


def registration_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start_callback))
    app.add_handler(
        CallbackQueryHandler(
            subscription_callback, pattern=callback_data.CHECK_SUBSCRIPTION
        )
    )
