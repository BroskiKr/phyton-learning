from pymongo import MongoClient
from datetime import datetime

# Підключення до MongoDB
client = MongoClient('mongodb://mongo:27017/')

# Створення бази даних 'usersDB'
db = client['usersDB']

# Створення колекції 'users'
users = db['users']

# Додавання початкових документів
initial_users = [
    {
        "first_name": "admin",
        "last_name": "admin",
        "created_at": datetime.now(),
        "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
        "email": "somegmail@gmail.com"
    },
    {
        "first_name": "Andrij",
        "last_name": "Krokhmalnyy",
        "created_at": datetime.now(),
        "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
        "email": "krohmalnyj.andr@gmail.com"
    },
    {
        "first_name": "Vasyl",
        "last_name": "Khomiv",
        "created_at": datetime.now(),
        "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
        "email": "somegmail@gmail.com"
    },
    {
        "first_name": "Elon",
        "last_name": "Musk",
        "created_at": datetime.now(),
        "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
        "email": "somegmail@gmail.com"
    },
    {
        "first_name": "Cristiano",
        "last_name": "Ronaldo",
        "created_at": datetime.now(),
        "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
        "email": "somegmail@gmail.com"
    }
]


if users.count_documents({}) == 0:
    users.insert_many(initial_users)


