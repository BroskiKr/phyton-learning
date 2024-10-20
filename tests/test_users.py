from fastapi.testclient import TestClient
from app.main import app
from app.mongo_db import users_collection
from app import utils

client = TestClient(app)


def get_user_test1_id():
    user = users_collection.find_one({"email": "test1@gmail.com"})
    id = user["_id"]
    return id


# tests
def test_create_user(auth_header):
    res = client.post(
        "/users",
        json={
            "first_name": "Test1",
            "last_name": "Test1",
            "email": "test1@gmail.com",
            "password": "test",
        },
    )
    created_user = users_collection.find_one({"email": "test1@gmail.com"})
    assert res.status_code == 201
    assert created_user["last_name"] == "Test1" and utils.verify(
        "test", created_user["password"]
    )


def test_get_users(auth_header):
    res = client.get("/users", headers=auth_header)
    test1_user = res.json()[-1]
    assert res.status_code == 200
    assert (
        test1_user["email"] == "test1@gmail.com" and test1_user["last_name"] == "Test1"
    )


def test_get_one_user(auth_header):
    res = client.get(f"/users/{get_user_test1_id()}", headers=auth_header)
    assert res.json()["email"] == "test1@gmail.com"
    assert res.status_code == 200


def test_change_user(auth_header):
    res = client.put(
        f"/users/{get_user_test1_id()}",
        headers=auth_header,
        json={
            "first_name": "Test2",
            "last_name": "Test2",
            "email": "test1@gmail.com",
            "password": "test1",
        },
    )
    updated_user = users_collection.find_one({"email": "test1@gmail.com"})
    assert res.status_code == 200
    assert updated_user["last_name"] == "Test2" and utils.verify(
        "test1", updated_user["password"]
    )


def test_delete_user(auth_header):
    res = client.delete(f"/users/{get_user_test1_id()}", headers=auth_header)
    deleted_user = users_collection.find_one({"email": "test1@gmail.com"})
    assert deleted_user == None
    assert res.status_code == 204
