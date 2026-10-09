import logging

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from database.engine import async_session
from database.requests import get_user

from fluentogram import TranslatorHub 

logger = logging.getLogger(__name__)

class TraslatorRunnerMiddleware(BaseMiddleware):
    def __init__(self, hub: TranslatorHub):
        super().__init__()
        self.hub = hub
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug('Початок роботи TraslatorRunnerMiddleware')
        user = data.get('user_in_db')
        if user:
            language_code = user.language
        else:
            user = data.get('event_from_user')
            language_code = user.language_code if user else 'en'
            
        i18n_translator = self.hub.get_translator_by_locale(language_code)
        data['i18n'] = i18n_translator
        logger.info(f'[TRM] Перекладач завантажено для мови: {language_code}')
        
        return await handler(event, data)