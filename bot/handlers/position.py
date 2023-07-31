from telegram import InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from constants import callback_data, constant, keyboards, messages, states
from handlers import menu
from services import aio_client, positions


async def position_callback(update, context, text=messages.POSITION_MESSAGE):
    """Функция-обработчик для кнопки Парсер позиций."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON),
    )
    return states.POSITION_RESULT


async def position_incorrent_callback(update, context):
    """Функция-обработчик для некорректного ввода номера склада."""
    await position_callback(
        update, context, text=messages.INCORRECT_POSITION_INPUT_MESSAGE
    )


async def position_parser_callback(update, context) -> str:
    """Функция-обработка запроса пользователя"""
    text_split = update.message.text.split()
    user_data = {
        "article": int(text_split[0]),
        "text": " ".join(text_split[1:]),
    }
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_REQUEST_MESSAGE.format(
            user_data.get("article"), user_data.get("text")
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
    )
    await position_result_to_db(update, context, user_data)
    return states.POSITION_SUBSCRIBE


async def get_parsing_result(user_data: dict) -> str:
    """Функция получения результата парсинга."""
    article = int(user_data.get("article"))
    search_phrase = user_data.get("text")
    parser_result = await positions.run_processes(article, search_phrase)
    return prepare_answer(article, search_phrase, parser_result)


async def define_subscriptions_frequency(update, context, user_data):
    """Функция запроса периодичности подписки."""
    parser_result = await get_parsing_result(user_data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=parser_result,
        reply_markup=InlineKeyboardMarkup(
            keyboards.POSITION_SUBSCRIPTION_KEYBOARD
        ),
    )


async def send_position_parser_subscribe(update, context):
    """Функция-проверки подписки на периодичный парсинг (1/6/12ч)"""
    frequency = update.callback_query.data

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_SUBSCRIBE_MESSAGE.format(frequency),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
    )
    return states.END


async def position_result_to_db(update, context, user_data):
    """Вывод результата парсинга, добавление к БД, кнопка Подписки(1/6/12ч)"""
    user_data["frequency"] = await define_subscriptions_frequency(
        update, context, user_data
    )
    await aio_client.post(constant.REQUEST_POSITION_URL, data=user_data)


def prepare_answer(article, search_phrase, parser_result):
    answer = f"Артикул: {article}\nЗапрос: {search_phrase}\n\n"
    for elem in parser_result:
        answer += (
            f"{list(elem.keys())[0]} - "
            f"Позиция: {str(list(elem.values())[0])}\n"
        )
    return answer


position_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            position_callback, pattern=callback_data.GET_POSITION
        )
    ],
    states={
        states.POSITION_RESULT: [
            CallbackQueryHandler(
                menu.cancel_callback, pattern=callback_data.CANCEL
            ),
            MessageHandler(
                filters.Regex(constant.POSITION_PATTERN),
                position_parser_callback,
            ),
            MessageHandler(filters.TEXT, position_incorrent_callback),
        ],
        states.POSITION_SUBSCRIBE: [
            CallbackQueryHandler(
                send_position_parser_subscribe, pattern=callback_data.SUBSCRIB1
            ),
            CallbackQueryHandler(
                send_position_parser_subscribe, pattern=callback_data.SUBSCRIB6
            ),
            CallbackQueryHandler(
                send_position_parser_subscribe,
                pattern=callback_data.SUBSCRIB12,
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.cancel_callback, pattern=callback_data.CANCEL
        ),
        CallbackQueryHandler(menu.menu_callback, pattern=callback_data.MENU),
    ],
    allow_reentry=True,
)


def position_handlers(app):
    app.add_handler(position_conv)
