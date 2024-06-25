from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
  res = client.post('/login',data={'username':'Test','password':'1234'})
  assert res.status_code == 200
  assert res.json().get('access_token')