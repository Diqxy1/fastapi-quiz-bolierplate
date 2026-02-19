import logging

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config.database_url import DatabaseUrl

logger = logging.getLogger(__name__)

db = DatabaseUrl().get_database_url()
db_engine = create_async_engine(
    db,
    echo=False,
    future=True
)
db_session = async_sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass

async def get_database():
    async with db_session() as session:
        try:
            yield session
        finally:
            await session.close()