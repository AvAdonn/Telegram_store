import logging
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

load_dotenv()
logger = logging.getLogger(__name__)

db_url = os.getenv('DB_URL')
if db_url is None:
    logger.critical('Відсутнє помилання | БазиДаних')
    raise ValueError('DBUrl error!')

engine = create_async_engine(
    db_url,
    echo=False
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('База даних успішно сформована!')