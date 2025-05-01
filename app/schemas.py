from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class ToDoBase(BaseModel):
    title: str
    description: Optional[str] = None

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class ToDoOut(ToDoBase):
    id: int
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True
