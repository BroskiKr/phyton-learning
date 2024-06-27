from fastapi.testclient import TestClient
from app.main import app
from app.mongo_db import users_collection

client = TestClient(app)


# help functions
def get_auth_header():
    login_response = client.post(
        "/login", data={"username": "Test", "password": "1234"}
    )
    token = login_response.json().get("access_token")
    auth_header = {"Authorization": f"Bearer {token}"}
    return auth_header


def get_test_user_id():
    user = users_collection.find_one({"email": "test@gmail.com"})
    id = user["_id"]
    return id


def get_test_post_id():
    res = client.get("/posts", headers=get_auth_header())
    return res.json()[0]["id"]


# tests
def test_create_post():
    res = client.post(
        "/posts",
        headers=get_auth_header(),
        json={"title": "Test", "body": "Test", "owner_id": str(get_test_user_id())},
    )
    assert res.json()["body"] == "Test"
    assert res.status_code == 201


def test_get_posts():
    res = client.get("/posts", headers=get_auth_header())
    assert res.status_code == 200
    assert res.json()[0]["body"] == "Test"


def test_change_post():
    res = client.put(
        f"/posts/{get_test_post_id()}",
        headers=get_auth_header(),
        json={"title": "Test1", "body": "Test1"},
    )
    assert res.json()["title"] == "Test1"
    assert res.status_code == 200


def test_delete_post():
    res = client.delete(f"/posts/{get_test_post_id()}", headers=get_auth_header())
    assert res.status_code == 204
