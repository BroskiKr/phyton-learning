from fastapi import status,HTTPException,Depends,APIRouter
from typing import Union,List
from app import models,schemas,oauth2
from app.postgresDb import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix='/posts',
  tags=['Posts']
)

## get 
@router.get('/',response_model=List[schemas.PostResponse]) 
def read_posts(user_id: Union[str, None] = None,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)) :
  # if user_id and user_id != "admin":
  #   users_posts = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
  #   return users_posts
  posts = db.query(models.Post).all()
  return posts
 
@router.get('/{post_id}',response_model=schemas.PostResponse) 
def read_post(post_id:int,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)): 
  post = db.query(models.Post).filter(models.Post.id == post_id).first()
  if post:
    return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
 
 
##post 
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse) 
def create_post(newPost: schemas.NewPost,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)): 
  # owner = db.query(models.User).filter(models.User.id == newPost.owner_id).first()
  # if not owner:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {newPost.owner_id} was not found') 
  post = models.Post(**newPost.dict())
  db.add(post)
  db.commit()
  db.refresh(post)
  return post  

##update
@router.put('/{post_id}',response_model=schemas.PostResponse)
def update_post(post_id:int,updatedPost: schemas.UpdatePost,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == post_id)
  post = post_query.first()
  if post:
    post_query.update(updatedPost.dict(),synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')
 
##delete 
@router.delete('/{post_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(post_id:int,db:Session = Depends(get_db),user_data:int = Depends(oauth2.get_current_user)): 
  post = db.query(models.Post).filter(models.Post.id == post_id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
  post.delete(synchronize_session=False)
  db.commit()
