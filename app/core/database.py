from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.db_url)
async_session = AsyncSession(engine)
AsyncSessionItem = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionItem() as async_session:
        yield async_session
