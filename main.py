from fastapi import FastAPI,status,HTTPException,Response 
from datetime import datetime 
from pydantic import BaseModel

app = FastAPI() 
 
class NewPost(BaseModel): 
  title:str 
  body:str 
 
posts = [ 
    { "id": 1, "title": "Як покращити концентрацію на робочому місці", "body": "Практичні поради та стратегії для підвищення концентрації та продуктивності під час роботи.", "data": "16.03.2024" }, 
    { "id": 2, "title": "Ідеї для здорового сніданку", "body": "Смачні та здорові ідеї для сніданку, щоб почати день з енергією та бадьорістю.", "data": "15.06.2024" }, 
    { "id": 3, "title": "Техніки саморозвитку, які змінять ваше життя", "body": "Дізнайтеся про ефективні техніки саморозвитку, які допоможуть вам стати кращою версією себе.", "data": "28.12.2024" }, 
    { "id": 4, "title": "10 місць, які варто відвідати у вашому місті", "body": "Відкрийте для себе найкращі місця та атракції у вашому місті для незабутнього часу проведеного.", "data": "05.09.2024" }, 
    { "id": 5, "title": "Секрети ефективного управління часом", "body": "Навчіться управляти своїм часом ефективно та досягати більше за короткий період.", "data": "20.11.2024" }, 
    { "id": 6, "title": "Рецепти здорових сніданків для дітей", "body": "Смачні та поживні рецепти сніданків, які діти обожнюють і які допоможуть їм розпочати день правильно.", "data": "02.04.2024" }, 
    { "id": 7, "title": "Як подолати стрес на роботі", "body": "Практичні поради та стратегії для ефективного управління стресом під час робочого дня.", "data": "17.10.2024" }, 
    { "id": 8, "title": "Тренування для підвищення енергії та витривалості", "body": "Ефективні вправи та тренування для збільшення енергії та витривалості протягом дня.", "data": "08.08.2024" }, 
    { "id": 9, "title": "5 книг для літнього читання", "body": "Список захоплюючих книг, які варто прочитати цього літа, щоб насолодитися відпочинком та розвитком.", "data": "12.01.2024" }, 
    { "id": 10, "title": "Як знайти баланс між роботою та особистим життям", "body": "Поради та стратегії для досягнення гармонії між кар'єрою та особистим життям для збереження здоров'я та щастя.", "data": "29.05.2024" } 
] 
 
@app.get('/') 
def read_root(): 
  return 'Home' 
 
## get 
@app.get('/posts') 
def read_posts(): 
  return posts 
 
@app.get('/posts/{post_id}') 
def read_post(post_id:int): 
  for post in posts: 
    if post["id"] == post_id: 
      return post 
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found') 
 
 
##(post for post in posts if post["id"] == post_id)  як воно працює 
 
##post 
@app.post('/posts',status_code=status.HTTP_201_CREATED) 
def create_post(newPost: NewPost): 
  post = dict(newPost) 
  post["id"] = max(post["id"] for post in posts) + 1 
  post["date"] = datetime.now() 
  posts.append(post) 
  return post  

##update
@app.put('/posts/{post_id}')
def update_posts(post_id:int,updatedPost:NewPost):
  upPost = dict(updatedPost)
  for post in posts: 
    if post['id'] == post_id: 
      post["title"] = upPost["title"]
      post["body"] = upPost["body"]
      return post
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')
 
##delete 
@app.delete('/posts/{post_id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(post_id:int): 
  for post in posts: 
    if post['id'] == post_id: 
      posts.remove(post) 
      return Response(status_code=status.HTTP_204_NO_CONTENT) 
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {post_id} was not found')