async def add_to_db(update):
    """Функция-подписки на ТГ-какнал и внесение в БД"""
    return True


async def position_parser(update):
    """Функция-вызов парсера (позиция в поиске)"""
    result = 33
    return result


async def ckeck_warehouse_request(update):
    """Функция-запрос к апи для получения коэффициента приемки"""
    result = 44
    return result


async def remainder_parser(update):
    """Функция-вызов парсера остатков по складам и размерам"""
    result = []
    return result


async def position_parser_subscribe(update):
    """Функция-подписки на периодичный парсинг позиции"""
    result = update.callback_query.data
    return result
