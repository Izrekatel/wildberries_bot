from typing import Optional

from constants import messages

from . import aio_client


def prepare_url(wh_id: int) -> str:
    """Подготавливает URL для зарпоса."""
    url = "https://wbcon.ru/wp-admin/admin-ajax.php?action=get_limit_store&id="
    return url + str(wh_id)


def add_cookies_in_headers() -> dict[str, str]:
    """Создает необходимые headers."""
    cookies = {"beget": "begetok"}
    headers = {"Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])}
    return headers


def check_response(response: dict) -> Optional[dict]:
    """Проверяем полученный ответ, т.к при запросе склада, которого"""
    """не существует, всё равно возвращается статус код 200"""
    try:
        response = response["detail"]
        return None
    except KeyError:
        return response


def prepare_result(response: dict) -> str:
    """Парсим ответ"""
    """Пробуем получить коэффициенты и устанавливаем значение "Недоступно"""
    """если данный вид упаковки недоступен"""
    try:
        mono_pallet = response["mono_pallet"][0]["coefficient"]
    except IndexError:
        mono_pallet = "Недоступно"

    try:
        super_safe = response["super_safe"][0]["coefficient"]
    except IndexError:
        super_safe = "Недоступно"

    try:
        koroba = response["koroba"][0]["coefficient"]
    except IndexError:
        koroba = "Недоступно"

    result = messages.STORE_RATE_RESULT_MESSAGE.format(
        mono_pallet, super_safe, koroba
    )
    return result


async def full_search(wh_id: int) -> Optional[str]:
    url = prepare_url(wh_id)
    headers = add_cookies_in_headers()
    response = await aio_client.get(url=url, headers=headers)
    checked_response = check_response(response)
    result = None
    if checked_response:
        result = prepare_result(checked_response)
    return result
