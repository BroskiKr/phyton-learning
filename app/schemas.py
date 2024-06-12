from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class NewPost(BaseModel): 
  title:str 
  body:str
  owner_id:int

class UpdatePost(BaseModel):
  title:str
  body:str

class NewUser(BaseModel): 
  first_name:str 
  last_name:str
  email:EmailStr
  password:str

class UserResponse(BaseModel):
  id:int
  first_name:str 
  last_name:str 
  email:EmailStr
  created_at: datetime

  class Config:
    orm_mode = True

class PostResponse(NewPost):
  id:int
  created_at: datetime
  owner: UserResponse
  
  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  username:str
  password:str

class Token(BaseModel):
  access_token:str
  token_type:str

class TokenData(BaseModel):
  id:Optional[str] = None


