from fastapi.testclient import TestClient
from app.main import app
from app.mongo_db import users_collection

client = TestClient(app)

#help functions
def get_auth_header():
  login_response = client.post('/login',data={'username':'Test','password':'1234'})
  token = login_response.json().get('access_token')
  auth_header = {'Authorization': f'Bearer {token}'}
  return auth_header

def get_test_user_id():
  user = users_collection.find_one({"email": "test1@gmail.com"})
  id = user['_id']
  return id


#tests
def test_get_users():
  res = client.get('/users',headers=get_auth_header())
  assert res.status_code == 200

def test_create_user():
  res = client.post('/users',headers=get_auth_header(),json={'first_name':"Test1","last_name":"Test1","email":"test1@gmail.com","password":"test"})
  assert res.json()['email'] == "test1@gmail.com"
  assert res.status_code == 201

def test_get_one_user():
  res = client.get(f'/users/{get_test_user_id()}',headers=get_auth_header())
  user = res.json()
  assert user['email'] == 'test1@gmail.com'
  assert res.status_code == 200

def test_change_user():
  res = client.put(f'/users/{get_test_user_id()}',headers=get_auth_header(),json={'first_name':"Test2","last_name":"Test2","email":"test1@gmail.com","password":"test"})
  assert res.json()['last_name'] == "Test2"
  assert res.status_code == 200


def test_delete_user():
  res = client.delete(f'/users/{get_test_user_id()}',headers=get_auth_header())
  assert res.status_code == 204




