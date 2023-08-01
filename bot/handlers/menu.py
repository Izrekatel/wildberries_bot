from telegram import InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from constants import keyboards, messages, states


async def menu(update, context, message=messages.MENU_MESSAGE):
    """Функция-обработчик главного меню."""
    await context.bot.send_message(
        update.effective_chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD),
    )
    return states.END


async def cancel(update, context):
    """Функция-обработчик для кнопки отмена."""
    return await menu(update, context)


async def unknown(update, context):
    """Функция-обработчик неизвестных боту команд."""
    return await menu(
        update, context, message=messages.UNKNOWN_COMMAND_MESSAGE
    )


async def send_text_in_menu(update, context):
    """Функция-обработчик неизвестного текста при отправке в меню."""
    """Хэндлер добавлен в telegram_bot в последнюю очередь."""
    await menu(update, context, message=messages.UNKNOWN_COMMAND_MESSAGE)


def menu_handlers(app: Application):
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
