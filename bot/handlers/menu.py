from telegram import InlineKeyboardMarkup
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from constants import callback_data, commands, keyboards, messages


async def menu_callback(update, context, message=messages.HELLO_MESSAGE):
    """Функция-обработчик главного меню."""
    await context.bot.send_message(
        update.effective_chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_KEYBOARD)
    )


async def cancel_callback(update, context):
    """Функция-обработчик для кнопки отмена."""
    await menu_callback(update, context, message=messages.CANCEL_MESSAGE)


async def unknown_callback(update, context):
    """Функция-обработчик неизвестных боту команд."""
    await menu_callback(update, context, message=messages.UNKNOWN_COMMAND_MESSAGE)


async def subscription_callback(update, context):
    """Функция-обработчик для кнопки Мои подписки на позиции."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.SUBSCRIPTIONS_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboards.MENU_BUTTON)
    )


def menu_handlers(app: Application) -> Application:
    app.add_handler(CommandHandler(commands.MENU, menu_callback))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern=callback_data.MENU))
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern=callback_data.CANCEL))
    app.add_handler(CallbackQueryHandler(subscription_callback, pattern=callback_data.GET_POSITION_SUBSCRIPTIONS))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_callback))
