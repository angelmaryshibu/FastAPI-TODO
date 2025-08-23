from fastapi import FastAPI , Request
from uuid import UUID
from basesub import Users,Login,Tasks,Display,UpdateTask
from sqlalchemy import select,func,update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel 
from contextlib import asynccontextmanager
from createdb import db,engine , Base
from models import User , Task, UserSession
from fastapi.exceptions import HTTPException
from typing import List
from passlib.context import CryptContext

@asynccontextmanager
async def lifespan(_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app=FastAPI(lifespan=lifespan)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    finally:
        await db.remove()

@app.post('/register/')
async def register_user(user:Users):
    hash=hash_password(user.password)
    db_user=User(name=user.name, email=user.email,password=hash)
    db.add(db_user)
    await db.commit()
    return {"message":"User Registered"}


@app.post('/login/')
async def login(user: Login):
    db_user=await db.execute(select(User).where(User.email==user.email))
    db_user=db_user.scalars().first()
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session = UserSession(user_id=db_user.id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {"Message":"Login Successful", "status": "success", "session": str(session.session_id)}

@app.post('/task/')
async def create_task(task:Tasks):
    db_session=await db.execute(select(UserSession).where(UserSession.session_id==task.sid))
    db_session=db_session.scalars().first()
    if not db_session:
        return {"message":"Session ID failed"}
    db.add(Task(user_id=db_session.user_id, title=task.title))
    await db.commit()
    return {"task":task.title,"message":"created"}

@app.delete('/task/')
async def delete_task(task:Tasks):
    db_session=await db.execute(select(UserSession).where(UserSession.session_id==task.sid))
    db_session=db_session.scalars().first()
    if not db_session:
        return {"message":"Session ID failed"}
    db_task=await db.execute(select(Task).where(Task.user_id==db_session.user_id,func.lower(Task.title) == func.lower(task.title)))
    db_task=db_task.scalars().first()
    if not db_task:
        return {"message":"no task found"}
    await db.delete(db_task)
    await db.commit()
    return{"message":"Task Deleted"}

@app.get('/task/')
async def display_task(sessionid:Display):
    db_session=await db.execute(select(UserSession).where(UserSession.session_id==sessionid.sid))
    db_session=db_session.scalars().first()
    if not db_session:
        return {"message":"Session ID failed"}
    db_user=await db.execute(select(User).where(User.id==db_session.user_id))
    db_user=db_user.scalars().first()

    task=await db.execute(select(Task).where(Task.user_id==db_user.id))
    task=task.scalars().all()

    task_titles=[{"title":user.title, "complete": user.completed} for user in task]
    
    return{
        "user":db_user.name,
        "tasks":task_titles
    }

@app.put("/task/")
async def update_task(uptask:UpdateTask):
    db_session=await db.execute(select(UserSession).where(UserSession.session_id==uptask.sid))
    db_session=db_session.scalars().first()
    if not db_session:
        return {"message":"Session ID failed"}
    new=await db.execute(update(Task).where(Task.user_id == db_session.user_id, func.lower(Task.title) == func.lower(uptask.title)).values(completed=uptask.status))
    if not new:
        return{"message":"Task not Found"}
    await db.commit()
    return{"message":"Task Updated"}


@app.post("/logout")
async def logout(id:Display):
    db_session=await db.execute(select(UserSession).where(UserSession.session_id==id.sid))
    db_session=db_session.scalars().first()
    if not db_session:
        return {"message":"Session ID failed"}
    await db.delete(db_session)
    await db.commit()
    return {"message":"logout successfully"}

