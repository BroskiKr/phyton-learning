from fastapi import Depends,APIRouter,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import requests
from app.settings import CLIENT_ID,CLIENT_SECRET

from app.database import get_db
from sqlalchemy.orm import Session
from app import models,oauth2

router = APIRouter(
  tags=['GoogleAuth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = CLIENT_ID
GOOGLE_CLIENT_SECRET = CLIENT_SECRET
GOOGLE_REDIRECT_URI = "http://localhost:3000/login"

@router.get("/login/google")
def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }



def verify_google_credentials(google_data:dict,db:Session):
    email = google_data['email']
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User did not exist")
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}

@router.get("/auth/google")
def auth_google(code: str,db:Session = Depends(get_db)):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    google_access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {google_access_token}"})
    user_info = user_info.json()
    token = verify_google_credentials(user_info,db)
    return token


