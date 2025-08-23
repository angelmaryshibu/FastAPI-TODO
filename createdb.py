from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker,async_scoped_session
import asyncio
from sqlalchemy.orm import declarative_base

engine = create_async_engine("postgresql+asyncpg://postgres:angel123@localhost:5432/postgres")

Session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
db=async_scoped_session(Session_factory, scopefunc=asyncio.current_task)
Base = declarative_base()


    
