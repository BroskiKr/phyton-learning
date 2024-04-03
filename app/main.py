from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Union
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI() 


while True:
  try:
    conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password ='krohmalA',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful! ")
    break
  except Exception as error:
    print("Connecting to database failed")
    print("Error:",error)
    time.sleep(2)

class NewPost(BaseModel): 
  title:str 
  body:str 
 

'''
def searchPost(text):
  cursor.execute('SELECT * FROM posts WHERE title LIKE %s OR body LIKE %s',(text,text))
  searched_posts = cursor.fetchall()
  if searched_posts: return searched_posts
  return {"error": "Such post doesnt exist"}
'''


@app.get('/') 
def read_root(): 
  return 'Home' 

## get 
@app.get('/posts') 
def read_posts(search: Union[str, None] = None):
  cursor.execute('SELECT * FROM posts') ## чи треба ставити """....."""
  posts = cursor.fetchall()
  ##if search:
    ##return searchPost(search.lower())
  return posts
 
@app.get('/posts/{post_id}') 
def read_post(post_id:int): 
  cursor.execute('SELECT * FROM posts WHERE id = %s ', (str(post_id),))  ##нашо кома
  post = cursor.fetchone()
  if post:
    return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
 
 
##post 
@app.post('/posts',status_code=status.HTTP_201_CREATED) 
def create_post(newPost: NewPost): 
  cursor.execute('INSERT INTO posts (body,title) VALUES (%s,%s) RETURNING *', (newPost.body,newPost.title))
  post = cursor.fetchone()
  conn.commit()
  return post  

##update
@app.put('/posts/{post_id}')
def update_posts(post_id:int,updatedPost:NewPost):
  cursor.execute('UPDATE posts SET title = %s, body = %s WHERE id = %s RETURNING *',(updatedPost.title,updatedPost.body,post_id))
  updatedPost = cursor.fetchone()
  conn.commit()
  if updatedPost:
    return updatedPost
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')
 
##delete 
@app.delete('/posts/{post_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(post_id:int): 
  cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *' ,(str(post_id),))
  deletedPost = cursor.fetchone()
  conn.commit()
  if deletedPost == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
  

