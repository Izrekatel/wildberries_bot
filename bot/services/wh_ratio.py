import aiohttp
import asyncio
import json


def prepare_url(url, wh_id):
    """Подготавливает для зарпоса URL. Передаём в него ID склада"""
    return url + str(wh_id)


def set_cookie():
    """Устанавливает необходимые куки"""
    cookies = {
        'beget': 'begetok'
    }
    headers = {'Cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()])}
    return headers


def check_response(response):
    """Проверяем полученный ответ, т.к при запросе склада, которого """
    """не существует, всё равно возвращается статус код 200"""
    response = json.loads(response)
    try:
        response = response["detail"]
        return None
    except KeyError:
        return response


def prepare_result(text):
    """Парсим ответ"""
    """Пробуем получить коэффициенты и устанавливаем значение "Недоступно"""
    """если данный вид упаковки недоступен"""
    try:
        mono_pallet = text["mono_pallet"][0]["coefficient"]
    except IndexError:
        mono_pallet = "Недоступно"

    try:
        super_safe = text["super_safe"][0]["coefficient"]
    except IndexError:
        super_safe = "Недоступно"

    try:
        koroba = text["koroba"][0]["coefficient"]
    except IndexError:
        koroba = "Недоступно"

    result = {
        "Монопаллет": mono_pallet,
        "Суперсейф": super_safe,
        "Короб": koroba,
    }
    return result


async def full_search(wh_id):
    url = "https://wbcon.ru/wp-admin/admin-ajax.php?action=get_limit_store&id="
    prepared_url = prepare_url(url, wh_id)
    cookie = set_cookie()

    async with aiohttp.ClientSession() as session:
        response = await session.get(prepared_url, headers=cookie)
        response = await response.text()
        response = check_response(response)
        if response:
            result = prepare_result(response)
            return result
        else:
            print("Некорректный запрос склада")
