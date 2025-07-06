from sqlalchemy import Column,Integer , String, ForeignKey,PrimaryKeyConstraint, Boolean, UUID,False_
from createdb import Base,engine

from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password=Column(String)

class Task(Base):
    __tablename__ = "tasks"

    user_id = Column(Integer,ForeignKey("users.id"), index=True)
    title = Column(String)
    completed = Column(Boolean, nullable=False,default=False)
    __table_args__=(
        PrimaryKeyConstraint("user_id","title"),
        )

class UserSession(Base):
    __tablename__ = "user_sessions"

    user_id = Column(Integer,ForeignKey("users.id"),unique=True,index=True)
    session_id = Column(UUID, primary_key=True, index=True, default=uuid4)