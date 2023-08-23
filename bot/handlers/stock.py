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
from services import aio_client, stock


async def stock_callback(update, context, text=messages.STOCK_MESSAGE):
    """Функция-обработчик для кнопки Парсер остатков."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON),
    )
    return states.STOCK_RESULT


async def stock_incorrent_callback(update, context):
    """Функция-обработчик для некорректного ввода номера склада."""
    return await stock_callback(
        update, context, text=messages.INCORRECT_ARTICLE_INPUT_MESSAGE
    )


async def stock_result_callback(update, context):
    """Функция-вывода результатов парсинга по артикулу"""
    parser_result = await stock.stock_parser(article=update.message.text)
    result = await prepare_result(parser_result)
    user_data = {
        "articul": update.message.text,
        "user_id": update.effective_user.id,
    }
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )
    await stock_request_to_db(user_data)
    return states.END


async def stock_request_to_db(user_data: dict) -> None:
    """Добавление запроса остатков к БД."""
    await aio_client.post(constant.REQUEST_STOCK_URL, data=user_data)


async def get_warehouse_name(id: str) -> str:
    """Получение названия склада из БД по номеру."""
    warehouse = await aio_client.get(f"{constant.WAREHOUSE_URL}{id}")
    if warehouse.get("name"):
        return warehouse["name"]
    return f"Склад №{id}"


async def prepare_result(parser_result: list) -> str:
    """Функция подготовки результата парсера по артикулу."""
    answer = "Результат:\nОстатки по складам\n\n"
    if not parser_result:
        return answer + "отсуствуют."
    for elem in parser_result:
        size = elem.get("Название")
        whs = elem.get("Склады")
        if size:
            answer += f"Размеры {size}:\n"
        for wh in whs:
            id = wh.get("ID Склада")
            ammount = wh.get("Количество")
            warehouse_name = await get_warehouse_name(id)
            answer += f"{warehouse_name}: {ammount} шт.\n"
        answer += "\n"
    return answer


stock_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(stock_callback, pattern=callback_data.GET_STOCK)
    ],
    states={
        states.STOCK_RESULT: [
            MessageHandler(filters.Regex(r"^\d+$"), stock_result_callback),
            MessageHandler(filters.TEXT, stock_incorrent_callback),
        ]
    },
    fallbacks=[
        CallbackQueryHandler(menu.cancel, pattern=callback_data.CANCEL),
    ],
    allow_reentry=True,
)


def stock_handlers(app: Application) -> None:
    app.add_handler(stock_conv)
