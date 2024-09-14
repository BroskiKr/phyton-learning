import pytest
from app.mongo_db import users_collection
from datetime import datetime
from app.postgres_db import SessionLocal
from app.oauth2 import create_access_token


@pytest.fixture(scope="session", autouse=True)
def manage_user():
    def create_test_user():
        new_user = {
            "first_name": "Test",
            "last_name": "Test",
            "created_at": datetime.now(),
            "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
            "email": "test@gmail.com",
        }
        result = users_collection.insert_one(new_user)
        created_user = users_collection.find_one({"_id": result.inserted_id})
        return created_user

    user = create_test_user()
    user_id = user["_id"]

    yield

    def delete_test_user():
        users_collection.delete_one({"_id": user_id})

    delete_test_user()


@pytest.fixture()
def test_user_id():
    user = users_collection.find_one(
        {
            "first_name": "Test",
            "last_name": "Test",
            "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
            "email": "test@gmail.com",
        }
    )
    user_id = user["_id"]
    return str(user_id)


@pytest.fixture(scope="module")
def auth_header():
    user = users_collection.find_one(
        {
            "first_name": "Test",
            "last_name": "Test",
            "password": "$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.",
            "email": "test@gmail.com",
        }
    )
    user_id = user["_id"]
    token = create_access_token({"user_id": str(user_id)})
    auth_header = {"Authorization": f"Bearer {token}"}
    return auth_header


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
