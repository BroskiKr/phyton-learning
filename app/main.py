from fastapi import FastAPI,status,HTTPException,Depends
from typing import Union,List
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI() 

models.Base.metadata.create_all(bind=engine)

# while True:
#   try:
#     conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password ='krohmalA',cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was successful! ")
#     break
#   except Exception as error:
#     print("Connecting to database failed")
#     print("Error:",error)
#     time.sleep(2)

# def searchPost(text):
#   cursor.execute('SELECT * FROM posts WHERE title LIKE %s OR body LIKE %s',(text,text))
#   searched_posts = cursor.fetchall()
#   if searched_posts: return searched_posts
#   return {"error": "Such post doesnt exist"}

@app.get('/') 
def read_root(): 
  return 'Home' 

## get 
@app.get('/posts',response_model=List[schemas.PostResponse]) 
def read_posts(search: Union[str, None] = None,db:Session = Depends(get_db)) :
  #cursor.execute('SELECT * FROM posts') 
  #posts = cursor.fetchall()
  ##if search:
    ##return searchPost(search.lower())
  posts = db.query(models.Post).all()
  return posts
 
@app.get('/posts/{post_id}',response_model=schemas.PostResponse) 
def read_post(post_id:int,db:Session = Depends(get_db)): 
  # cursor.execute('SELECT * FROM posts WHERE id = %s ', (str(post_id),))  ##нашо кома
  # post = cursor.fetchone()
  post = db.query(models.Post).filter(models.Post.id == post_id).first()
  if post:
    return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
 
 
##post 
@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse) 
def create_post(newPost: schemas.NewPost,db:Session = Depends(get_db)): 
  # cursor.execute('INSERT INTO posts (body,title) VALUES (%s,%s) RETURNING *', (newPost.body,newPost.title))
  # post = cursor.fetchone()
  # conn.commit()
  post = models.Post(**newPost.dict())
  db.add(post)
  db.commit()
  db.refresh(post)
  return post  

##update
@app.put('/posts/{post_id}',response_model=schemas.PostResponse)
def update_post(post_id:int,updatedPost: schemas.UpdatePost,db:Session = Depends(get_db)):
  # cursor.execute('UPDATE posts SET title = %s, body = %s WHERE id = %s RETURNING *',(updatedPost.title,updatedPost.body,post_id))
  # updatedPost = cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == post_id)
  post = post_query.first()
  if post:
    post_query.update(updatedPost.dict(),synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')
 
##delete 
@app.delete('/posts/{post_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(post_id:int,db:Session = Depends(get_db)): 
  # cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *' ,(str(post_id),))
  # deletedPost = cursor.fetchone()
  # conn.commit()
  post = db.query(models.Post).filter(models.Post.id == post_id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
  post.delete(synchronize_session=False)
  db.commit()


# Users

## get 
@app.get('/users') 
def read_users(search: Union[str, None] = None,db:Session = Depends(get_db)) :
  users = db.query(models.User).all()
  return users
 
@app.get('/users/{user_id}') 
def read_user(user_id:int,db:Session = Depends(get_db)): 
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if user:
    return user
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {user_id} was not found') 
 
 
##post 
@app.post('/users',status_code=status.HTTP_201_CREATED) 
def create_user(newUser: schemas.NewUser,db:Session = Depends(get_db)): 
  user = models.User(**newUser.dict())
  db.add(user)
  db.commit()
  db.refresh(user)
  return user  

##update
@app.put('/users/{user_id}')
def update_user(user_id:int,updatedUser: schemas.NewUser,db:Session = Depends(get_db)):
  user_query = db.query(models.User).filter(models.User.id == user_id)
  user = user_query.first()
  if user:
    user_query.update(updatedUser.dict(),synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {user_id} was not found')
 
##delete 
@app.delete('/users/{user_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_user(user_id:int,db:Session = Depends(get_db)): 
  user = db.query(models.User).filter(models.User.id == user_id)
  if user.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
  user.delete(synchronize_session=False)
  db.commit()
  

