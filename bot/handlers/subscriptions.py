from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler

from constants import callback_data, keyboards

# from constants import callback_data, constant, keyboards, messages
# from services import aio_client
# from handlers import menu


async def subscriptions_callback(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции."""
    data = {"user_id": f"{update.effective_user.id}"}
    # subscriptions = await aio_client.get(constant.MY_SUBSCRIPTIONS_URL, data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data,
        # text=messages.SUBSCRIPTIONS_MESSAGE.format(subscriptions),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )


def subscriptions_handlers(app: Application) -> None:
    app.add_handler(
        CallbackQueryHandler(
            subscriptions_callback,
            pattern=callback_data.GET_POSITION_SUBSCRIPTIONS,
        )
    )
