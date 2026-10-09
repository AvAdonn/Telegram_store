import logging

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from database.engine import async_session
from database.requests import get_user

logger = logging.getLogger(__name__)

class DBMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any ]
    ) -> Any:
        logger.debug('Початок роботи DBMiddleware')
        async with async_session() as session:
            data['session'] = session
            
            tg_user = data.get('event_from_user')
            if tg_user:
                user = await get_user(session, tg_user.id)
                data['user_in_db'] = user
                logger.info('[DBM]Користувача(user | None) завантажено в дату')
            else:
                data['user_in_db'] = None
                logger.info('[DBM]Користувача(None) авантажено в дату')
                
        return await handler(event, data)
    
