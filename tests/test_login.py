from fastapi.testclient import TestClient
from app.main import app
from app.oauth2 import get_current_user, create_access_token
from datetime import datetime

client = TestClient(app)


def test_login(test_user_id, mocker):
    mocked_datetime = mocker.patch("app.oauth2.datetime")
    mocked_datetime.utcnow.return_value = datetime(2030, 1, 1, 12, 0, 0)

    res = client.post("/login", data={"username": "Test", "password": "1234"})
    token = res.json().get("access_token")

    data_from_token = get_current_user(token)
    id_from_token = data_from_token.id

    assert res.status_code == 200
    assert id_from_token == test_user_id
    assert token == create_access_token({"user_id": test_user_id})
