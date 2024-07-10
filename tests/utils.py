from datetime import datetime
from app.mongo_db import users_collection


def create_test_user():
    new_user =  {
        "first_name": "Test",
        "last_name": "Test",
        "created_at": datetime.now(),
        "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
        "email": "test@gmail.com",
    }
    result = users_collection.insert_one(new_user)
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return created_user

def delete_test_user():
    users_collection.delete_one({"email": "test@gmail.com"})

def get_auth_header(client):
    login_response = client.post(
        "/login", data={"username": "Test", "password": "1234"}
    )
    token = login_response.json().get("access_token")
    auth_header = {"Authorization": f"Bearer {token}"}
    return auth_header


