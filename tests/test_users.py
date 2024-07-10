from fastapi.testclient import TestClient
from app.main import app
from app.mongo_db import users_collection
from tests import utils

client = TestClient(app)

test_user = utils.create_test_user()
auth_header = utils.get_auth_header(client)


def get_user_test1_id():
    user = users_collection.find_one({"email": "test1@gmail.com"})
    id = user["_id"]
    return id


# tests
def test_create_user():
    res = client.post(
        "/users",
        headers=auth_header,
        json={
            "first_name": "Test1",
            "last_name": "Test1",
            "email": "test1@gmail.com",
            "password": "test",
        },
    )
    assert res.json()["email"] == "test1@gmail.com"
    assert res.status_code == 201


def test_get_users():
    res = client.get("/users", headers=auth_header)
    assert res.json()[-1]['email'] == "test1@gmail.com"
    assert res.status_code == 200


def test_get_one_user():
    res = client.get(f"/users/{get_user_test1_id()}", headers=auth_header)
    assert res.json()["email"] == "test1@gmail.com"
    assert res.status_code == 200


def test_change_user():
    res = client.put(
        f"/users/{get_user_test1_id()}",
        headers=auth_header,
        json={
            "first_name": "Test2",
            "last_name": "Test2",
            "email": "test1@gmail.com",
            "password": "test",
        },
    )
    assert res.json()["last_name"] == "Test2"
    assert res.status_code == 200


def test_delete_user():
    res = client.delete(f"/users/{get_user_test1_id()}", headers=auth_header)
    utils.delete_test_user()
    assert res.status_code == 204

