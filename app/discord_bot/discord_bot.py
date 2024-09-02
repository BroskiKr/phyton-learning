import discord 
from discord.ext import commands
import requests
from app.settings import DISCORD_TOKEN
from app.oauth2 import create_access_token

bot=commands.Bot(command_prefix='/',intents=discord.Intents().all())

discord_token = DISCORD_TOKEN

BASE_URL = "http://127.0.0.1:8000/posts"

user_tokens = {}

async def fetch_data(ctx,url,method='GET', json=None):
    token = user_tokens.get(ctx.author.id)
    if not token:
        await ctx.send("You need to auth first using the /auth command.")
        return
    headers = {
      'Authorization': f'Bearer {token}'
    }
    if method == 'GET':
        response = requests.get(url,headers=headers)
    elif method == 'POST':
        response = requests.post(url, json=json,headers=headers)
    elif method == 'PUT':
        response = requests.put(url, json=json,headers=headers)
    elif method == 'DELETE':
        response = requests.delete(url,headers=headers)
    
    return response


@bot.command()
async def auth(ctx):
    token = create_access_token(data={"user_id": str(ctx.author.id)})
    user_tokens[ctx.author.id] = token

@bot.command()
async def hello(ctx):
  await ctx.reply(f'Hello {ctx.author.name}')

@bot.command()
async def clear(ctx, amount: int = 100):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'Deleted {len(deleted)} messages', delete_after=5)


@bot.command()
async def get_posts(ctx, limit: int = 10, page: int = 1):
    url = f"{BASE_URL}?limit={limit}&page={page}"
    response = await fetch_data(ctx,url)
    if response is None:
       return
    try:
        posts = response.json()
    except:
        posts = []
    if posts:
        for post in posts:
            await ctx.send(f"Post ID: {post['id']}, Title: {post['title']}")
    else:
        await ctx.send(f"User {ctx.author.name} dont create posts yet")
        return 


@bot.command()
async def get_post(ctx, post_id: int):
    url = f"{BASE_URL}/{post_id}"
    response = await fetch_data(ctx,url)
    if response is None:
       return
    try:
        post = response.json()
        await ctx.send(f"Title: {post['title']}\nContent: {post['body']}")
    except:
        await ctx.send(f"Post with id:{post_id} does not exist")
    

@bot.command()
async def create_post(ctx, title: str, body: str):
    new_post = {
        "title": title,
        "body": body,
    }
    response = await fetch_data(ctx,BASE_URL, method='POST', json=new_post)
    if response is None:
       return
    if response.status_code == 201:
        post = response.json()
        await ctx.send(f"Post created with ID: {post['id']}")
    else:
        await ctx.send(f"Failed to create post")

@bot.command()
async def update_post(ctx, post_id: int, title: str = None, body: str = None):
    updated_post = {}
    if title:
        updated_post['title'] = title
    if body:
        updated_post['body'] = body
    if not updated_post:
        await ctx.send("Nothing to update")
        return
    url = f"{BASE_URL}/{post_id}"
    response = await fetch_data(ctx,url, method='PUT', json=updated_post)
    if response is None:
       return
    try:
        post = response.json()
        await ctx.send(f"Post {post['id']} updated:\nTitle: {post['title']}\nContent: {post['body']} ")
    except:
        await ctx.send(f"Post with id:{post_id} does not exist")
    
  
@bot.command()
async def delete_post(ctx, post_id: int):
    url = f"{BASE_URL}/{post_id}"
    response = await fetch_data(ctx,url, method='DELETE')
    if response is None:
       return
    if response.status_code == 204:
        await ctx.send(f"Post with ID {post_id} deleted.")
    elif response.status_code == 404 :
        await ctx.send(f"Post with id:{post_id} does not exist")
    else:
        await ctx.send(f"Failed to delete post with ID {post_id}.")

  
bot.run(discord_token)