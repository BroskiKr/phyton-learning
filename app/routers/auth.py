from fastapi import status,HTTPException,Depends,APIRouter,Response
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
  prefix='/login',
  tags=['Login']
)


@router.post('/',response_model=schemas.Token)
def login(user_login:OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.last_name == user_login.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid input")
  if not utils.verify(user_login.password,user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid input")

  access_token = oauth2.create_access_token(data={"user_id":user.id})
  return {"access_token":access_token, "token_type":"bearer"}