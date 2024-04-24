from dotenv import dotenv_values

config = dotenv_values(".env")
SQLALCHEMY_DATABASE_URL = config.get('SQLALCHEMY_DATABASE_URL')
