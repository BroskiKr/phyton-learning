from fastapi.testclient import TestClient
from app.main import app
from tests import utils

client = TestClient(app)

test_user = utils.create_test_user()
auth_header = utils.get_auth_header(client)

def get_test_post_id():
    res = client.get('/posts',headers=auth_header)
    post = res.json()[-1]
    return post["id"]


# tests
def test_create_post():
    res = client.post(
        "/posts",
        headers=auth_header,
        json={"title": "Test", "body": "Test", "owner_id": '1'},
    )
    assert res.json()["body"] == "Test"
    assert res.status_code == 201


def test_get_posts():
   res = client.get("/posts", headers=auth_header)
   assert res.status_code == 200
   assert res.json()[0]["body"] == "Test"


def test_change_post():
    res = client.put(
        f"/posts/{get_test_post_id()}",
        headers=auth_header,
        json={"title": "Test1", "body": "Test1"},
    )
    assert res.json()["title"] == "Test1"
    assert res.status_code == 200


def test_delete_post():
    res = client.delete(f"/posts/{get_test_post_id()}", headers=auth_header)
    result = client.get("/posts", headers=auth_header)
    utils.delete_test_user()
    assert result.json() == []
    assert res.status_code == 204
