from fastapi import status, HTTPException, Depends, APIRouter
from app import schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.mongo_db import users_collection

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/", response_model=schemas.Token)
def login(user_login: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": user_login.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid input"
        )
    if not utils.verify(user_login.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid input"
        )
    user_id = str(user["_id"])
    access_token = oauth2.create_access_token(data={"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}
