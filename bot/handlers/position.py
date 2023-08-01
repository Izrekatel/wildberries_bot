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
    return await position_callback(
        update, context, text=messages.INCORRECT_POSITION_INPUT_MESSAGE
    )


async def position_parser_callback(update, context) -> str:
    """Функция-обработка запроса пользователя"""
    text_split = update.message.text.split()
    context.user_data["articul"] = int(text_split[0])
    context.user_data["text"] = " ".join(text_split[1:])
    context.user_data["user_id"] = update.effective_user.id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_REQUEST_MESSAGE.format(
            context.user_data.get("articul"), context.user_data.get("text")
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
    )
    await define_subscriptions_frequency(update, context)
    return states.POSITION_SUBSCRIBE


async def get_parsing_result(user_data: dict) -> str:
    """Функция получения результата парсинга."""
    article = int(user_data.get("articul"))
    search_phrase = user_data.get("text")
    parser_result = await positions.run_processes(article, search_phrase)
    return prepare_answer(article, search_phrase, parser_result)


async def define_subscriptions_frequency(update, context):
    """Функция запроса периодичности подписки."""
    parser_result = await get_parsing_result(context.user_data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=parser_result,
        reply_markup=InlineKeyboardMarkup(
            keyboards.POSITION_SUBSCRIPTION_KEYBOARD
        ),
    )


async def send_position_parser_subscribe(update, context):
    """Функция подписки на периодичный парсинг (1/6/12ч)."""
    context.user_data["frequency"] = update.callback_query.data
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_SUBSCRIBE_MESSAGE.format(
            context.user_data.get("frequency")
        ),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )
    await position_result_to_db(context.user_data)
    return states.END


async def position_result_to_db(user_data: dict) -> None:
    """Добавление подписки к БД."""
    await aio_client.post(constant.REQUEST_POSITION_URL, data=user_data)


def prepare_answer(
    article: int, search_phrase: str, parser_result: list
) -> str:
    """Подготовка ответа за запрос."""
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
        CallbackQueryHandler(menu.cancel, pattern=callback_data.CANCEL),
    ],
    allow_reentry=True,
)


def position_handlers(app: Application) -> None:
    app.add_handler(position_conv)
