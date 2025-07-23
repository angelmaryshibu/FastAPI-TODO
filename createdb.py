from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base

engine = create_engine("postgresql+psycopg://postgres:angel123@localhost:5432/postgres")

SessionLocal = sessionmaker(bind=engine,  autocommit=False)
Base = declarative_base()


    
