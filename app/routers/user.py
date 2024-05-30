from fastapi import status,HTTPException,Depends,APIRouter
from typing import Union,List
from .. import models, schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix='/users',
  tags=['Users']
)

## get 
@router.get('/',response_model=List[schemas.UserResponse]) 
def read_users(search: Union[str, None] = None,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)) :
  users = db.query(models.User).all()
  print(type(users))
  print(users)
  return users
 
@router.get('/{user_id}',response_model=schemas.UserResponse) 
def read_user(user_id:int,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)): 
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if user:
    return user
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {user_id} was not found') 
 
 
##post 
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse) 
def create_user(newUser: schemas.NewUser,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)): 
  hashed_password = utils.hash(newUser.password)
  newUser.password = hashed_password
  user = models.User(**newUser.dict())
  db.add(user)
  db.commit()
  db.refresh(user)
  return user  

##update
@router.put('/{user_id}',response_model=schemas.UserResponse)
def update_user(user_id:int,updatedUser: schemas.NewUser,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
  user_query = db.query(models.User).filter(models.User.id == user_id)
  user = user_query.first()
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {user_id} was not found')
  hashed_password = utils.hash(updatedUser.password)
  updatedUser.password = hashed_password
  user_query.update(updatedUser.dict(),synchronize_session=False)
  db.commit()
  db.refresh(user)
  return user

##delete 
@router.delete('/{user_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_user(user_id:int,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)): 
  user = db.query(models.User).filter(models.User.id == user_id)
  if user.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
  user.delete(synchronize_session=False)
  db.commit()