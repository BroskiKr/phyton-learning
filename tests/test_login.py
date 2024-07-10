from fastapi.testclient import TestClient
from app.main import app
from tests import utils

client = TestClient(app)

def test_login():
    utils.create_test_user()
    res = client.post("/login", data={"username": "Test", "password": "1234"})
    utils.delete_test_user()
    assert res.status_code == 200
    assert res.json().get("access_token")
    


