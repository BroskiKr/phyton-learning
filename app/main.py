from fastapi import FastAPI,status,HTTPException,Response 
from datetime import datetime 
from pydantic import BaseModel
from typing import Union
import json

app = FastAPI() 
 
class NewPost(BaseModel): 
  title:str 
  body:str 
 
def takeData(filePath = 'data.txt'):
  data = None
  with open(filePath,'r',encoding='utf-8') as file:
    data = json.load(file)
  return data

def editData(data,filePath = 'data.txt'):
  with open(filePath, 'w', encoding='utf-8') as file: 
    json.dump(data,file,indent=4, ensure_ascii=False)

def searchPost(text):
  searchedPosts = []
  for post in posts:
    if text in post["title"].lower() or text in post["body"].lower():
      searchedPosts.append(post)
  if searchedPosts: return searchedPosts
  return {"error": "Such post doesnt exist"}

posts = takeData()

@app.get('/') 
def read_root(): 
  return 'Home' 

## get 
@app.get('/posts') 
def read_posts(search: Union[str, None] = None):
  if search:
    return searchPost(search.lower())
  return posts
 
@app.get('/posts/{post_id}') 
def read_post(post_id:int): 
  for post in posts: 
    if post["id"] == post_id: 
      return post 
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
 
 
##post 
@app.post('/posts',status_code=status.HTTP_201_CREATED) 
def create_post(newPost: NewPost): 
  post = dict(newPost) 
  post["id"] = max(post["id"] for post in posts) + 1 
  post["date"] = datetime.now().isoformat()
  posts.append(post)
  editData(posts) 
  return post  

##update
@app.put('/posts/{post_id}')
def update_posts(post_id:int,updatedPost:NewPost):
  upPost = dict(updatedPost)
  for post in posts: 
    if post['id'] == post_id: 
      post["title"] = upPost["title"]
      post["body"] = upPost["body"]
      editData(posts) 
      return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')
 
##delete 
@app.delete('/posts/{post_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(post_id:int): 
  for post in posts: 
    if post['id'] == post_id: 
      posts.remove(post) 
      editData(posts) 
      return Response(status_code=status.HTTP_204_NO_CONTENT) 
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')

