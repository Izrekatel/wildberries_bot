COMMAND_NAME = "@Gelrud_Boris"
BOT_NAME = "WildberriesBot"
TELEGRAM_CHANEL_SUBSCRIBE = "https://t.me/dbfsfg"
# После получения доступа к каналу подписки с правами админа
# TELEGRAM_CHANEL_SUBSCRIBE = 'https://t.me/mpexperts'

BACKEND_URL = "nginx"
# BACKEND_URL = "localhost"
# if you start local telegram_bot change BACKEND_URL=localhost

FREQUENCY_URL = f"http://{BACKEND_URL}/api/frequency/"
REQUEST_POSITION_URL = f"http://{BACKEND_URL}/api/request_position/"
REQUEST_STOCK_URL = f"http://{BACKEND_URL}/api/request_stock/"
REQUEST_RATE_URL = f"http://{BACKEND_URL}/api/request_rate/"
REQUEST_TELEGRAM_USER_URL = f"http://{BACKEND_URL}/api/telegram_user/"

SELENIUM_URL = f"http://{BACKEND_URL}/selenium-grid/"

POSITION_PATTERN = r"^(?P<articul>\d+)(?P<phrase>(\s+[a-zA-Zа-яА-ЯёЁ]+)+)"

# Parser constants.
MAIN_URL = "https://www.wildberries.ru"
BROWSER_LOADING_TIME = 15.0
GEO_LOADING_TIME = 15.0
SCROLL_LOADING_TIME = 2.0
MAX_ADDITIONAL_PAGES_SEARCHING = 4
GOODS_ON_PAGE = 100

# CITY сделать моделью, добавить связь с пользователем,
# сделать выбор городов-подписок.
CITY = {
    "Санкт-Петербург": "Санкт-Петербург, метро Сенная площадь",
    "Москва": "Москва, метро Лубянка",
    "Казань": "г. Казань (Республика Татарстан)",
    "Краснодар": "Краснодар центр",
    "Екатеринбург": "Екатеринбург центр",
    "Владивосток": "город Владивосток",
}

# WAREHOUSES сделать моделью, выяснить откуда данные и заполнить.
WAREHOUSES = {
    1733: "Екатеринбург",
    507: "Коледино",
    124731: "Крёкшино КБТ",
    686: "Новосибирск",
    2737: "Санкт-Петербург",
    117986: "Казань",
    130744: "Краснодар",
    117501: "Подольск",
    204939: "Казахстан",
    159402: "Санкт-Петербург Шушары",
    205228: "Белая Дача",
    120762: "Электросталь",
    121709: "Электросталь КБТ",
    206348: "Тула",
    206968: "Чехов",
    208941: "Домодедово",
    208277: "Невинномысск",
    210001: "Чехов 2",
    210515: "Вёшки",
    211622: "Минск",
    1193: "Хабаровск",
    207743: "Пушкино",
    218210: "Обухово",
    218623: "Подольск 3",
}
