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


async def rate_callback(update, context):
    """Функция-обработчик для кнопки Отслеживание коэффицианта приемки WB"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.RATE_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.CANCEL_BUTTON),
    )
    return states.RATE_RESULT


async def rate_result_callback(update, context):
    """Функция-вывод результата Отслеживание коэффициента приемки WB"""
    parser_result = await wh_ratio.full_search(update.message.text)
    result = await prepare_answer(parser_result)
    if result is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.UNKNOWN_COMMAND_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result,
            reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON),
        )
    return states.END


async def prepare_answer(parser_result):
    answer = (
        f"Коэффицианты приемки:\nМонопаллет: "
        f'{parser_result.get("Монопаллет")}\nСуперсейф: '
        f'{parser_result.get("Суперсейф")}\nКороб: '
        f'{parser_result.get("Короб")}\n'
    )
    return answer


rate_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(rate_callback, pattern=callback_data.GET_RATE)
    ],
    states={
        states.RATE_RESULT: [
            MessageHandler(filters.TEXT, rate_result_callback)
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
