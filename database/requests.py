import logging
import aiogram

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from database.models import User

logger = logging.getLogger(__name__)

async def get_user(session: AsyncSession, tg_id: int) -> User | None:
    if not tg_id:
        return None 
    
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    
    return user

async def add_user(
    session: AsyncSession,
    tg_id: int,
    language: str,
    referral_id: int | None        
) -> None:
    new_user = insert(User).values(tg_id=tg_id, referral_id=referral_id, language=language)
    new_user = new_user.on_conflict_do_nothing(index_elements=['tg_id'])
    
    try:
        await session.execute(new_user)
        await session.commit()
        logger.info(f'Нового користувача({tg_id}) зареєстровано в базі')
    except SQLAlchemyError as e:
        await session.rollback()
        logger.info(f'Помилка при додаванні користувача({tg_id}): {e}', exc_info=True)
        

async def change_language(code: str, user: User, session: AsyncSession) -> bool:
    try:
        user.language = code
        await session.merge(user)
        await session.commit()
        logger.debug('Зміну мови збережено в базі')
        
        return True
    
    except Exception as e:
        logger.error(f'Невдалося змінити мову користувача: {user.tg_id} -> {e}')
        await session.rollback()
        
        return False