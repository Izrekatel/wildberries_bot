# import asyncio
import sys
import time
from multiprocessing import Manager, Process
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from constants import constant, messages

# Для локального запуска:
# 1. Раскоментируйте 1 строку (импорт asyncio).
# 2. Раскоментируйте get_positions и его запуск (в конце файла).
# 3. Укажите артикул и поисковую фразу.
# 4. Cкопируйте в папку services constant.py и messages.py.
# 5. Поменяйте в constant.py BACKEND_URL на localhost.
# 6. Закоментируйте 14 стоку и раскоментируйте 22.
# import constant, messages


def start_browser(
    article: int, search_phrase: str, adress: str, stocks: list
) -> None:
    """Запуск браузера в работу."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--headless")  # для запуска без UI
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Remote(
        command_executor=constant.SELENIUM_URL, options=chrome_options
    )
    result = full_search(article, search_phrase, adress, browser)
    stocks.append(result)
    browser.quit()


def open_url(url: str, browser: Chrome) -> None:
    """Загружает страницу."""
    browser.get(url)
    time.sleep(constant.BROWSER_LOADING_TIME)


def prepare_city(city: str, browser: Chrome) -> None:
    """Выбирает на странице город, в котором будет производиться поиск."""
    geo_city = browser.find_element(
        By.CLASS_NAME,
        "simple-menu__link.simple-menu__link--address."
        "j-geocity-link.j-wba-header-item",
    )
    geo_city.click()
    time.sleep(constant.GEO_LOADING_TIME)
    search_input = browser.find_element(
        By.CLASS_NAME, "ymaps-2-1-79-searchbox-input__input"
    )
    search_input.send_keys(city)
    search_input.send_keys(Keys.ENTER)
    time.sleep(constant.BROWSER_LOADING_TIME)

    try:
        geo_list = browser.find_element(By.ID, "pooList")
        first_item = geo_list.find_element(
            By.CLASS_NAME, "address-item.j-poo-option"
        )
        first_item.click()
        time.sleep(constant.BROWSER_LOADING_TIME)
        select_button = browser.find_element(
            By.XPATH, "//button[text()='Выбрать']"
        )
        select_button.click()
        time.sleep(constant.BROWSER_LOADING_TIME)

    except NoSuchElementException:
        print("Элемент не найден: prepare_city")
        sys.exit()


def search_articul(search_phrase: str, browser: Chrome) -> None:
    """Осуществляет поиск заданной фразы на сайте."""
    search_input = browser.find_element(By.ID, "searchInput")
    search_input.send_keys(search_phrase)
    search_input.send_keys(Keys.ENTER)
    time.sleep(constant.BROWSER_LOADING_TIME)


def get_full_page(browser: Chrome) -> None:
    """Проматывает страницу в самый низ."""
    while True:
        body = browser.find_element(By.TAG_NAME, "body")
        actions = ActionChains(browser)
        time.sleep(constant.SCROLL_LOADING_TIME)
        for _ in range(2):
            actions.move_to_element(body).send_keys(Keys.PAGE_DOWN).perform()

        if browser.execute_script(
            "return (window.innerHeight + window.scrollY) >= "
            "document.body.scrollHeight;"
        ):
            break


def place_in_search(article: int, browser: Chrome) -> Optional[int]:
    """Находит артикул на странице и возвращает его порядковый номер."""
    """или None"""
    goods = browser.find_element(By.CLASS_NAME, "product-card-list")
    goods_list = goods.find_elements(By.CSS_SELECTOR, "article")
    articles = list(
        int(good.get_attribute("data-nm-id")) for good in goods_list
    )
    if article in articles:
        return goods_list.index(goods.find_element(By.ID, f"c{article}")) + 1


def find_next_page_button(browser: Chrome) -> bool:
    """Проверяет, есть ли кнопка перехода на следующую страницу"""
    """Если кнопка есть, то переходит по ссылке из неё."""
    try:
        element = browser.find_element(
            By.XPATH,
            '//a[contains(@class, "pagination-next pagination__next '
            'j-next-page") and contains(text(), "Следующая страница")]',
        )
        href = element.get_attribute("href")
        if href:
            open_url(url=href, browser=browser)
            return True
    except NoSuchElementException:
        print("Кнопка следующей страницы не найдена.")
        return False


def change_adress_to_city(adress: str) -> str:
    """Возвращает ключ по значению из словаря городов."""
    for city, val in constant.CITY.items():
        if val == adress:
            return city
    return adress


def prepare_result(place: int, page: int, city: str) -> dict[str, int]:
    """Возвращает отформатированный ответ"""
    position = page * constant.GOODS_ON_PAGE + place
    result = {city: position}
    return result


def full_search(
    article: int, search_phrase: str, adress: str, browser: Chrome
) -> dict:
    """Запуск полного цикла поиска"""
    open_url(url=constant.MAIN_URL, browser=browser)
    prepare_city(adress, browser)
    search_articul(search_phrase, browser)
    page = 0
    place = None
    city = change_adress_to_city(adress)
    result = {
        city: messages.ARTICUL_NOT_FOUND_MESSAGE.format(article, search_phrase)
    }
    while True:
        get_full_page(browser)
        place = place_in_search(article, browser)
        if place:
            break
        if page > constant.MAX_ADDITIONAL_PAGES_SEARCHING:
            return result
        next_page = find_next_page_button(browser)
        if not next_page:
            return result
        page += 1
    return prepare_result(place, page, city)


async def run_processes(article: int, search_phrase: str) -> list:
    """Запуск поиска позиций по всем городам."""
    manager = Manager()
    stocks = manager.list()
    processes = []

    for adress in constant.CITY.values():
        process = Process(
            target=start_browser, args=(article, search_phrase, adress, stocks)
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    return stocks


# For local running
# async def get_positions():
#     article = 21292604
#     search_phrase = "носки мужские"
#     positions = await run_processes(article, search_phrase)
#     print(positions)
#
#
# if __name__ == "__main__":
#     asyncio.run(get_positions())
