from constants.constant import (
    BOT_NAME,
    COMMAND_NAME,
    TELEGRAM_CHANEL_SUBSCRIBE,
)

START_BOT_DESCRIPTION_MESSAGE = (
    f"Привет! На связи команда {COMMAND_NAME}\n"
    f"Мы создали этого бота для помощи всем действующим поставщикам "
    f"Wildberries.\n\n"
    f"Здесь вы можете:\n"
    f"- отследить позиции вашей карточки в выдаче.\n"
    f"- увидеть остатки товара по складам\n"
    f"- узнать остатки товара по размерам.\n\n"
    f"Для начала работы нажмите Start"
)
START_MESSAGE = (
    f"Привет! Чтобы воспользоваться ботом, нужно подписаться на наш "
    f"telegram канал {TELEGRAM_CHANEL_SUBSCRIBE}"
)
SUCCESS_SUBSCRIBE_MESSAGE = (
    "Спасибо за подписку! Вы можете воспользоваться меню бота:"
)
FALSE_SUBSCRIBE_MESSAGE = "Вы не подписались на наш telegram канал"
HELLO_MESSAGE = (
    f"Добро пожаловать в {BOT_NAME}!\n"
    f"Узнайте на каких позициях находится ваш товар в поиске Wildberries."
)
MENU_MESSAGE = f"Вы находитесь в главном меню бота {BOT_NAME}!"
POSITION_MESSAGE = (
    "Для определения позиции артикула отправьте сообщение в формате\n"
    "'Артикул Поисковая фраза'\n\n"
    "Например:\n36704403 футболка женская"
)
POSITION_REQUEST_MESSAGE = (
    "Запрос с артикулом *{}* и поисковой фразой "
    "*{}* создан! В ближайшее время Вам будет отправлен результат"
)
POSITION_RESULT_MESSAGE = "Результат запроса. Товар на {} месте"
POSITION_SUBSCRIBE_MESSAGE = "Вы подписались на обновление каждые {} час(ов)"
STOCK_MESSAGE = (
    "Отправьте артикул для вывода остатков:\n" "Например:\n" "36704403\n"
)
STOCK_RESULT_MESSAGE = "остатки по складам и по размерам {}"
RATE_MESSAGE = (
    "Для получения коэффициентов приемки склада Wildberries "
    "отправьте сообщение содержащее id склада\n"
    "Например:\n"
    "507"
)
INCORRECT_POSITION_INPUT_MESSAGE = (
    "Запросите позицию в формате артикул(цифры) и запрос (текст)."
)
INCORRECT_STORE_INPUT_MESSAGE = (
    "ID склада указан некорректно. Укажите только цифры."
)
INCORRECT_ARTICLE_INPUT_MESSAGE = (
    "Артикул указан некорректно. Укажите только цифры."
)
RATE_RESULT_MESSAGE = "Коэффицианта приемки для склада {} составляет {}"
SUBSCRIPTIONS_MESSAGE = "Ваши подписки:\n{}"
NO_SUBSCRIPTIONS_MESSAGE = "У Вас не оформленно действующих подписок."
UNKNOWN_COMMAND_MESSAGE = "Неизвестная команда, воспользуйтесь меню"
TO_MAIN_MENU_MESSAGE = "Спасибо за подписку!"
ARTICUL_NOT_FOUND_MESSAGE = (
    "Артикул *{}* по поисковому запросу *{}* не найден."
)
NO_STORE_MESSAGE = "Нет склдада с номером {}."
STORE_RATE_RESULT_MESSAGE = (
    "Коэффицианты приемки:\nМонопаллет: {}\nСуперсейф: {}\nКороб: {}\n"
)
