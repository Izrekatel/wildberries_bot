from telegram import InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from constants import callback_data, keyboards, messages


async def menu_callback(update, context, message=messages.MENU_MESSAGE):
    """Функция-обработчик главного меню."""
    await context.bot.send_message(
        update.effective_chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )


async def cancel_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context)


async def unknown_callback(update, context):
    """Функция-обработчик неизвестных боту команд."""
    await menu_callback(
        update, context, message=messages.UNKNOWN_COMMAND_MESSAGE
    )


def menu_handlers(app: Application) -> Application:
    app.add_handler(
        CallbackQueryHandler(menu_callback, pattern=callback_data.MENU)
    )
    app.add_handler(
        CallbackQueryHandler(cancel_callback, pattern=callback_data.CANCEL)
    )
    app.add_handler(MessageHandler(filters.COMMAND, unknown_callback))
