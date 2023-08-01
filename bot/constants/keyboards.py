from telegram import InlineKeyboardButton

from constants import callback_data, constant

START_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Подписаться тут", url=constant.TELEGRAM_CHANEL_SUBSCRIBE
        )
    ],
    [
        InlineKeyboardButton(
            "Я подписался, запустить бота",
            callback_data=callback_data.CHECK_SUBSCRIPTION,
        )
    ],
]

MENU_BUTTON = [
    [InlineKeyboardButton("Перейти в меню", callback_data=callback_data.MENU)],
]

CANCEL_BUTTON = [
    [InlineKeyboardButton("Отмена", callback_data=callback_data.CANCEL)],
]

MENU_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Парсер позиций", callback_data=callback_data.GET_POSITION
        )
    ],
    [
        InlineKeyboardButton(
            "Парсер остатков", callback_data=callback_data.GET_STOCK
        )
    ],
    [
        InlineKeyboardButton(
            "Отслеживание коэффицианта приемки WB",
            callback_data=callback_data.GET_RATE,
        )
    ],
    [
        InlineKeyboardButton(
            "Мои подписки на позиции",
            callback_data=callback_data.GET_POSITION_SUBSCRIPTIONS,
        )
    ],
]

POSITION_REQUEST_BUTTON = [
    [
        InlineKeyboardButton(
            "Отправить еще запрос",
            callback_data=callback_data.GET_POSITION,
        )
    ],
    [InlineKeyboardButton("Перейти в меню", callback_data=callback_data.MENU)],
]

POSITION_SUBSCRIPTION_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Подписаться на обновления с интервалом:",
            callback_data="no action",
        )
    ],
    [
        InlineKeyboardButton("1 час", callback_data=callback_data.SUBSCRIB1),
        InlineKeyboardButton("6 часов", callback_data=callback_data.SUBSCRIB6),
        InlineKeyboardButton(
            "12 часов", callback_data=callback_data.SUBSCRIB12
        ),
    ],
    [
        InlineKeyboardButton(
            "Отменить подписку и перейти в меню",
            callback_data=callback_data.CANCEL,
        )
    ],
]
