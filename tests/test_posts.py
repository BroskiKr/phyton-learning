from fastapi.testclient import TestClient
from app.main import app
from app import models

client = TestClient(app)

def get_test_post_id(db,test_user_id):
    post = db.query(models.Post).filter(models.Post.owner_id == test_user_id).first()
    return post.id

# tests
def test_create_post(auth_header,db,test_user_id):
    res = client.post(
        "/posts",
        headers=auth_header,
        json={"title": "Test", "body": "Test", "owner_id": test_user_id}
    )
    post = db.query(models.Post).filter(models.Post.owner_id == test_user_id).first()
    assert post.title == "Test" and post.body == "Test" and post.owner_id == test_user_id
    assert res.json()["body"] == "Test"
    assert res.status_code == 201


def test_get_posts(auth_header):
   res = client.get("/posts", headers=auth_header)
   posts = res.json()
   assert res.status_code == 200
   assert len(posts) == 1
   assert posts[0]["body"] == "Test"


def test_change_post(auth_header,db,test_user_id):
    test_post_id = get_test_post_id(db,test_user_id)
    res = client.put(
        f"/posts/{test_post_id}",
        headers=auth_header,
        json={"title": "Test1", "body": "Test1"},
    )
    post = db.query(models.Post).filter(models.Post.owner_id == test_user_id).first()
    assert post.title == 'Test1' and post.body == 'Test1'
    assert res.status_code == 200


def test_delete_post(auth_header,db,test_user_id):
    test_post_id = get_test_post_id(db,test_user_id)
    res = client.delete(f"/posts/{test_post_id}", headers=auth_header)
    post = db.query(models.Post).filter(models.Post.owner_id == test_user_id).first()
    assert post == None
    assert res.status_code == 204
