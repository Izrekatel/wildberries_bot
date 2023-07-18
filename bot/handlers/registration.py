from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler

from config import BOT_URL, CHAT_ID
from constants import callback_data, commands, constant, keyboards, messages
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


async def subscription_callback(update, context):
    """Функция-проверки и внесения в БД нового подписчика"""
    data = {"chat_id": f"{CHAT_ID}", "user_id": f"{update.effective_user.id}"}
    subscribe = await aio_client.get(BOT_URL, data)
    if subscribe["result"]["status"] == "member":
        await aio_client.post(constant.REQUEST_TELEGRAM_USER_URL, data)
        await menu.menu_callback(update, context)
    else:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=messages.FALSE_SUBSCRIBE_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboards.START_KEYBOARD),
        )


def registration_handlers(app):
    app.add_handler(CommandHandler(commands.START, start_callback))
    app.add_handler(
        CallbackQueryHandler(
            subscription_callback, pattern=callback_data.CHECK_SUBSCRIPTION
        )
    )
