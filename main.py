from fastapi import FastAPI , Depends
from basesub import UserOut,Users,Login,DTask,Tasks,Display,UpdateTask
from sqlalchemy import Select
from sqlalchemy.orm import Session 
from pydantic import BaseModel 
from contextlib import asynccontextmanager
from createdb import SessionLocal,engine , Base
from models import User , Task, UserSession
from fastapi.exceptions import HTTPException
from typing import List
from passlib.context import CryptContext

@asynccontextmanager
async def lifespan(_):
    Base.metadata.create_all(bind=engine)
    yield 

app=FastAPI(lifespan=lifespan)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/Register/')
def register_user(user:Users , db:Session=Depends(get_db)):
    hash=hash_password(user.password)
    db_user=User(name=user.name, email=user.email,password=hash)
    db.add(db_user)
    db.commit()
    return {"message":"User Registered"}


@app.post('/Login/')
def login(user: Login,db: Session = Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session = UserSession(user_id=db_user.id)
    db.add(session)
    db.commit()
    return {"Message":"Login Successful", "status": "success", "session": session.session_id}

@app.post('/task/')
def create_task(task:Tasks , db:Session=Depends(get_db)):
    db_session=db.query(UserSession).filter(UserSession.session_id==task.sid).first()
    if not db_session:
        return {"message":"Session ID failed"}
    db.add(Task(user_id=db_session.user_id, title=task.title))
    db.commit()
    return {"task":task.title}

@app.delete('/task/')
def delete_task(task:DTask,db:Session=Depends(get_db)):
    db_session=db.query(UserSession).filter(UserSession.session_id==task.sid).first()
    if not db_session:
        return {"message":"Session ID failed"}
    title=task.title
    db_task=db.query(Task).filter(Task.user_id==db_session.user_id,Task.title==task.title).first()
    if not db_task:
        return {"no task found"}
    db.delete(db_task)
    db.commit()

@app.get('/task/')
def display_task(sessionid:Display,db:Session=Depends(get_db)):
    db_session=db.query(UserSession).filter(UserSession.session_id==task.sid).first()
    if not db_session:
        return {"message":"Session ID failed"}
    db_user=db.query(User).filter(User.id==db_session.session_id).first()
    task=db.query(Task).filter(Task.user_id==db_user.id).all()


    task_titles=[{"title":user.title, "complete": user.completed} for user in task]
    
    return{
        "user":db_user.name,
        "tasks":task_titles
    }
@app.put("/task/")
def update_task(uptask:UpdateTask,db:Session=Depends(get_db)):
    db_session=db.query(UserSession).filter(UserSession.session_id==uptask.sid).first()
    if not db_session:
        return {"message":"Session ID failed"}
    db.query(Task).filter(
    Task.user_id == db_session.user_id,
    Task.title == uptask.title
    ).update({"completed": True})
    db.commit()
    return{"message":"Task Updated"}


@app.post("/logout")
def logout(id:Display,db:Session=Depends(get_db)):
    db_session=db.query(UserSession).filter(UserSession.session_id==id.sid).first()
    if not db_session:
        return {"message":"Session ID failed"}
    db.delete(db_session)
    db.commit()
    return {"message":"logout successfully"}





