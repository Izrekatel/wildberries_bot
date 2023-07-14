import asyncio
import logging

import aiohttp
from telegram.ext import Application

from config import BOT_TOKEN
from constants.messages import START_BOT_DESCRIPTION_MESSAGE
from handlers import menu, position, rate, registration, stock

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def set_bot_description():
    """Функция изменения описания бота перед запуском."""
    method = 'setMyDescription'
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/{method}'
    data = {'description': START_BOT_DESCRIPTION_MESSAGE}
    async with aiohttp.ClientSession() as session:
        async with await session.post(url, json=data) as response:
            if response.status == 200:
                logger.info('Описание успешно установлено')
            else:
                logger.info('Ошибка при установке описания')


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_bot_description())
    bot = Application.builder().token(BOT_TOKEN).build()
    logger.info('Бот успешно запущен.')
    registration.registration_handlers(bot)
    menu.menu_handlers(bot)
    position.position_handlers(bot)
    stock.stock_handlers(bot)
    rate.rate_handlers(bot)
    bot.run_polling()


if __name__ == '__main__':
    main()
