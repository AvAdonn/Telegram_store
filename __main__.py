import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from utils.logger import setup_logger
from database.engine import init_models
from utils.i18n import create_translator_hub

from middleware.outer_md import DBMiddleware
from middleware.auth import AuthMiddleware
from middleware.i18n_md import TraslatorRunnerMiddleware
from handlers import get_routers

setup_logger()
logger = logging.getLogger(__name__)
logger.info('Логування завершено. Підготовка запуску...')


async def on_start() -> None:
    await init_models()
    logger.info('Старт бота завершено.')
    
async def on_finish() -> None:
    logger.info('Бота зупинено.')

async def main() -> None:
    load_dotenv()
    token = os.getenv('TOKEN')
    if token is None:
        raise ValueError('Token error')

    bot = Bot(token)
    dp = Dispatcher()
    
    try:
        dp.update.outer_middleware(DBMiddleware())
        
        translator_hub = create_translator_hub()
        dp.update.middleware(TraslatorRunnerMiddleware(hub=translator_hub))
        
        dp.message.middleware(AuthMiddleware())
        dp.callback_query.middleware(AuthMiddleware())
        
        dp.include_routers(*get_routers())
        
        dp.startup.register(on_start)
        dp.shutdown.register(on_finish)
        
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, hub=translator_hub)    
    except Exception as e:
        logger.critical(
            f'Критична помилка під час запуску: {e}',
            exc_info=True
        )
        
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Зупинено власноруч.')