from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import sessionmaker ,declarative_base

engine = create_async_engine("postgresql+psycopg://postgres:angel123@localhost:5432/postgres")

SessionLocal = async_sessionmaker(bind=engine,  autocommit=False)
Base = declarative_base()


    
