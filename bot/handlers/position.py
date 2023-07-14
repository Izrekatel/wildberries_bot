from telegram import InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from constants import (callback_data, commands, constant, keyboards, messages,
                       states)
from handlers.menu import menu_callback
from services import aio_client, services, many_cities_position


async def position_callback(update, context):
    """Функция-обработчик для кнопки Парсер позиций."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.POSITION_CANCEL_BUTTON)
    )
    return states.POSITION_RESULT


async def position_parser_callback(update, context):
    """Функция-обработка запроса пользователя"""
    text_split = update.message.text.split()
    user_data = {
        "articul": int(text_split[0]),
        "text": ' '.join(text_split[1:])
    }
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_REQUEST_MESSAGE.format(
            user_data.get("articul"), user_data.get("text")
        ),
        parse_mode="Markdown"
    )
    await position_result_to_db(update, context, user_data)
    return states.POSITION_SUBSCRIBE


async def position_result_to_db(update, context, user_data):
    """Вывод результата парсинга, добавление к БД, кнопка Подписки(1/6/12ч)"""
    articul = user_data.get("articul")
    search_phrase = user_data.get("text")
    parser_result = await many_cities_position.run_processes(articul, search_phrase)
    result = await prepare_answer(articul, search_phrase, parser_result)
    await aio_client.post(constant.REQUEST_POSITION_URL, data=user_data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result,
        reply_markup=InlineKeyboardMarkup(
            keyboards.POSITION_SUBSCRIPTION_KEYBOARD
        )
    )
    return states.END


async def prepare_answer(article, search_phrase, parser_result):
    answer = f'Артикул: {article}\nЗапрос: {search_phrase}\n\n'
    for elem in parser_result:
        answer += f'{list(elem.keys())[0]} - Позиция: {str(list(elem.values())[0])}\n'
    return answer


async def send_position_parser_subscribe(update, context):
    """Функция-проверки подписки на периодичный парсинг (1/6/12ч)"""
    frequency = await services.position_parser_subscribe(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.POSITION_SUBSCRIBE_MESSAGE.format(frequency),
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
    )
    return states.END


async def cancel_position_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context, message=messages.CANCEL_MESSAGE)
    return states.END


position_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            position_callback,
            pattern=callback_data.GET_POSITION
        )],
        states={
            states.POSITION_RESULT: [
                MessageHandler(
                    filters.Regex(constant.POSITION_PATTERN),
                    position_parser_callback
                )
            ],
            states.POSITION_SUBSCRIBE: [
                CallbackQueryHandler(
                    position_callback,
                    pattern=callback_data.GET_POSITION
                ),
                CallbackQueryHandler(
                    send_position_parser_subscribe,
                    pattern=callback_data.SUBSCRIB1
                ),
                CallbackQueryHandler(
                    send_position_parser_subscribe,
                    pattern=callback_data.SUBSCRIB6
                ),
                CallbackQueryHandler(
                    send_position_parser_subscribe,
                    pattern=callback_data.SUBSCRIB12
                ),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel_position_callback,
                pattern=callback_data.CANCEL_POSITION
            ),
            CommandHandler(commands.MENU, menu_callback),
            CommandHandler(commands.START, menu_callback),
        ],
        allow_reentry=True
    )


def position_handlers(app):
    app.add_handler(position_conv)
