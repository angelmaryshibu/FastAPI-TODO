from pydantic import BaseModel
from uuid import UUID

class Users(BaseModel):  
    name: str
    email: str
    password: str
    
class Login(BaseModel):
    email: str
    password: str   

class Tasks(BaseModel):
    sid : str
    title:str 

class Display(BaseModel):
    sid: UUID

class UpdateTask(BaseModel):
    sid: UUID
    title: str
    status: bool
