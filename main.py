from typing import Union
from fastapi import FastAPI

app = FastAPI()

posts = [
  {'id':1,'title':'some text','body':'some text',},
  {'id':2,'title':'some text','body':'some text',},
  {'id':3,'title':'some text','body':'some text',}
]

@app.get('/')
def read_root():
  return {'Hello' : 'world'}

@app.get('/items/{item_id}')
def read_item(item_id:int , q:Union[str,None] = None):
  return {'item_id' : item_id, 'q':q}

@app.get('/posts')
def read_posts():
  return posts

@app.get('/posts/{post_id}')
def read_post(post_id:int):
  return posts[post_id - 1]
  




