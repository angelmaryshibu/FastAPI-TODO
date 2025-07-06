from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base

engine = create_engine("sqlite:///todo.db")

SessionLocal = sessionmaker(bind=engine,  autocommit=False)
Base = declarative_base()


    