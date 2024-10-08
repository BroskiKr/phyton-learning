from dotenv import dotenv_values

config = dotenv_values(".env")
SQLALCHEMY_DATABASE_URL = config.get("SQLALCHEMY_DATABASE_URL")
MONGODB_URL = config.get("MONGODB_URL")

SECRET_KEY = config.get("SECRET_KEY")

CLIENT_ID = config.get("CLIENT_ID")
CLIENT_SECRET = config.get("CLIENT_SECRET")

DISCORD_TOKEN = config.get("DISCORD_TOKEN")
