from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler

from constants import callback_data, constant, keyboards, messages
from services import aio_client


async def subscriptions_callback(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции."""
    url = f"{constant.REQUEST_POSITION_URL}/{update.effective_user.id}"
    subscriptions = await aio_client.get(url)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=prepare_message(subscriptions),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )


def prepare_message(subscriptions: list) -> str:
    """Подготовка ответа на запрос списка подписок."""
    if subscriptions != []:
        answer = [
            "Номер. Артикул. Текст. Частоста обновления, час."
            "Последнее обновление."
        ]
        number = 1
        for subscription in subscriptions:
            row = (
                f"{number}. {subscription['articul']}. {subscription['text']}."
                f" {subscription['frequency']}. "
                f"{subscription['last_request']}."
            )
            number += 1
            answer.append(row)
        return messages.SUBSCRIPTIONS_MESSAGE.format("\n".join(answer))
    return messages.NO_SUBSCRIPTIONS_MESSAGE


def subscriptions_handlers(app: Application) -> None:
    app.add_handler(
        CallbackQueryHandler(
            subscriptions_callback,
            pattern=callback_data.GET_POSITION_SUBSCRIPTIONS,
        )
    )
