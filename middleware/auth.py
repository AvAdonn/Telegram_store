import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from fluentogram import TranslatorRunner

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug('Початок роботи AuthMiddleware')
        user = data.get('user_in_db')
        
        if user is None:
            if isinstance(event, Message) and event.text and event.text.startswith('/start'):
                return await handler(event, data)
            
            i18n: TranslatorRunner | None = data.get('i18n') 
            
            if isinstance(event, (Message, CallbackQuery)) and i18n:
                text = i18n.get('reg_text')
                await event.answer(text)
            else:
                logger.error('Помилка авторизації: відсутній i18n/невідомий тип події')
            return
        
        return await handler(event, data)