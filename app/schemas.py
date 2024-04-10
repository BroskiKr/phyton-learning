from pydantic import BaseModel
from datetime import datetime

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

class PostResponse(NewPost):
  id:int
  created_at: datetime
  owner: NewUser

  class Config:
    orm_mode:True




