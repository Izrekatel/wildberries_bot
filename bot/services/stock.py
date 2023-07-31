from . import aio_client


async def prepare_params(article: int) -> dict:
    """Делаем запрос к API wildberries для подготовки параметров"""
    """Добавляем наш артикул к параметрам запроса"""
    url = "https://user-geo-data.wildberries.ru/get-geo-info"
    json_data = await aio_client.get(url=url)
    params = {
        param.split("=")[0]: param.split("=")[1]
        for param in json_data["xinfo"].split("&")
    }
    params["nm"] = article
    return params


def parse_json(json: dict) -> list:
    """Парсим json, достаём необходимые данные, приводим к читаемому виду"""
    sizes_list = []
    stocks_list = []
    if json["data"]["products"]:
        for size in json["data"]["products"][0]["sizes"]:
            if size["stocks"]:
                stocks_list = [
                    {"ID Склада": item["wh"], "Количество": item["qty"]}
                    for item in size["stocks"]
                ]
                sizes_list.append(
                    {
                        "Название": size["name"],
                        "Обозначение": size["origName"],
                        "Склады": stocks_list,
                    }
                )
    return sizes_list


async def stock_parser(article: int) -> list:
    """Запуск парсера остатков по складам"""
    url = "https://card.wb.ru/cards/detail"
    params = await prepare_params(article)
    json_data = await aio_client.get(url=url, params=params)
    return parse_json(json_data)
