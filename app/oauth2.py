from jose import jwt,JWTError
from datetime import datetime,timedelta
from app import schemas
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "784162aac9017769558ffb6e08240f46637deb1397db5aa74a36e41fd0b7e24b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
  to_encode = data.copy()
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode["expire"] = expire.timestamp()
  jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return jwt_token

def verify_access_token(token:str,credentials_exception):
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    id:str = payload.get("user_id")
    if not id:
      raise credentials_exception
    token_data = schemas.TokenData(id=id)
  except JWTError:
    raise credentials_exception
  
  return token_data
  
def get_current_user(token:str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail='Could not validate credentials',headers={"WWW-Authenticate":"Bearer"})
  return verify_access_token(token,credentials_exception)
