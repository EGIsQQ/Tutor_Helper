from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

#Создаем асинхронную сессию для работы с БД
engine = create_async_engine('postgresql+asyncpg://admin:@localhost:5432/tutor_helper', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass