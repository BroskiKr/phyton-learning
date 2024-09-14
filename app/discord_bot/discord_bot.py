import discord
from discord.ext import commands
from discord import app_commands
import requests
from app.settings import DISCORD_TOKEN
from app.oauth2 import create_access_token
from app import schemas
from app.mongo_db import users_collection

bot = commands.Bot(command_prefix="/", intents=discord.Intents().all())

discord_token = DISCORD_TOKEN

BASE_URL = "http://127.0.0.1:8000/posts"

users_data = {}


async def fetch_data(interaction, url, method="GET", json=None):
    user = users_data.get(interaction.user.id)
    if user:
        token = user.get("token")
    if not user or not token:
        await interaction.response.send_message(
            "You need to login using the /auth command\nOR if you haven't registered yet, do it using the /register command",
            ephemeral=True,
        )
        return
    headers = {"Authorization": f"Bearer {token}"}
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=json, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=json, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)

    if response.status_code == 401:
        await interaction.response.send_message(
            "Your session has expired.\nYou need to auth using the /auth command.",
            ephemeral=True,
        )
        return

    return response


@bot.tree.command(name="auth", description="Authorize user")
async def auth(interaction: discord.Interaction):
    user = users_collection.find_one({"discord_id": interaction.user.id})
    if user:
        token = create_access_token(data={"user_id": str(user["_id"])})
        users_data[interaction.user.id] = {"token": token, "page": 1}
        await interaction.response.send_message(
            f"User {interaction.user.name} authorized"
        )
    else:
        await interaction.response.send_message(
            f"Error: You need to register first using /register command.",
            ephemeral=True,
        )


@bot.tree.command(name="register", description="Register a new user")
@app_commands.describe(
    first_name="Your first name",
    last_name="Your last name",
    email="Your email",
    password="Your password",
)
async def register(
    interaction: discord.Interaction,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    url = "http://127.0.0.1:8000/users"
    new_user = schemas.NewUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        discord_id=interaction.user.id,
    )
    response = requests.post(url, json=new_user.dict())
    if response.status_code == 201:
        created_user = response.json()
        if created_user["discord_id"] == interaction.user.id:
            token = create_access_token(data={"user_id": str(created_user["id"])})
            users_data[interaction.user.id] = {"token": token, "page": 1}
            await interaction.response.send_message(
                f"You were successfully registered", ephemeral=True
            )
    elif response.status_code == 409:
        error_data = response.json()
        detail_message = error_data.get("detail")
        await interaction.response.send_message(
            f"Error: {detail_message}", ephemeral=True
        )


@bot.tree.command(name="clear", description="Clear a chat history")
async def clear(interaction: discord.Interaction):
    if interaction.user.guild_permissions.manage_messages:
        deleted = await interaction.channel.purge()
        await interaction.response.send_message(
            f"Deleted {len(deleted)} messages", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )


@bot.tree.command(
    name="get_posts",
    description="Every time you print this command you get 10 your posts",
)
async def get_posts(interaction: discord.Interaction):
    user = users_data.get(interaction.user.id)
    if user:
        page = user.get("page")
    else:
        page = 1
    url = f"{BASE_URL}?limit={10}&page={page}"
    response = await fetch_data(interaction, url)
    if response is None:
        return
    posts = response.json()
    if posts:
        user["page"] = page + 1
        posts_message = "\n".join(
            [f"Post ID: {post['id']}, Title: {post['title']}" for post in posts]
        )
        await interaction.response.send_message(posts_message)
    else:
        await interaction.response.send_message(f"You dont create posts yet")


@bot.tree.command(name="get_post", description="Get post using its id")
@app_commands.describe(post_id="ID of the post you are looking for")
async def get_post(interaction: discord.Interaction, post_id: int):
    url = f"{BASE_URL}/{post_id}"
    response = await fetch_data(interaction, url)
    if response is None:
        return
    if response.status_code == 200:
        post = response.json()
        await interaction.response.send_message(
            f"Post ID: {post['id']}\nTitle: {post['title']}\nContent: {post['body']}"
        )
    elif response.status_code == 404:
        await interaction.response.send_message(
            f"Post with id:{post_id} does not exist", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"Failed to get post", ephemeral=True)


@bot.tree.command(name="create_post", description="Create new post")
@app_commands.describe(title="Post title", body="Post body")
async def create_post(interaction: discord.Interaction, title: str, body: str):
    new_post = {
        "title": title,
        "body": body,
    }
    response = await fetch_data(interaction, BASE_URL, method="POST", json=new_post)
    if response is None:
        return
    if response.status_code == 201:
        post = response.json()
        await interaction.response.send_message(
            f"Post created with ID: {post['id']}\nTitle: {post['title']}\nContent: {post['body']}"
        )
    else:
        await interaction.response.send_message(
            f"Failed to create post", ephemeral=True
        )


@bot.tree.command(name="update_post", description="Update an existing post")
@app_commands.describe(
    post_id="ID of the post you want to change", title="Post title", body="Post body"
)
async def update_post(
    interaction: discord.Interaction, post_id: int, title: str = None, body: str = None
):
    updated_post = {}
    if title:
        updated_post["title"] = title
    if body:
        updated_post["body"] = body
    if not updated_post:
        await interaction.response.send_message("Nothing to update")
        return
    url = f"{BASE_URL}/{post_id}"
    response = await fetch_data(interaction, url, method="PUT", json=updated_post)
    if response is None:
        return
    if response.status_code == 200:
        post = response.json()
        await interaction.response.send_message(
            f"Post {post['id']} updated:\nTitle: {post['title']}\nContent: {post['body']} "
        )
    elif response.status_code == 404:
        await interaction.response.send_message(
            f"Post with id:{post_id} does not exist", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"Failed to update post", ephemeral=True
        )


@bot.tree.command(name="delete_post", description="Delete an existing post")
@app_commands.describe(post_id="ID of the post you want to delete")
async def delete_post(interaction: discord.Interaction, post_id: int):
    url = f"{BASE_URL}/{post_id}"
    response = await fetch_data(interaction, url, method="DELETE")
    if response is None:
        return
    if response.status_code == 204:
        await interaction.response.send_message(f"Post with ID {post_id} deleted.")
    elif response.status_code == 404:
        await interaction.response.send_message(
            f"Post with id:{post_id} does not exist", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"Failed to delete post with ID {post_id}.", ephemeral=True
        )


@bot.tree.command(name="list", description="Print all available commands")
async def list(interaction: discord.Interaction):
    help_text = """
    Available commands:
    /auth - Authorize user
    /register [first_name] [last_name] [email] [password] - Register user
    /get_posts - Retrieve posts
    /get_post [post_id] - Retrieve a specific post
    /create_post [title] [body] - Create a new post
    /update_post [post_id] [title] [body] - Update a post
    /delete_post [post_id] - Delete a post
    """
    await interaction.response.send_message(help_text, ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()


bot.run(discord_token)
