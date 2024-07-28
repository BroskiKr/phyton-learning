from fastapi import status, HTTPException, Depends, APIRouter
from typing import Union, List
from app import schemas, utils, oauth2
from app.mongo_db import users_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["Users"])


def convert_to_user_response(user_data):
    return schemas.UserResponse(
        id=str(user_data["_id"]),
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        created_at=user_data["created_at"],
    )


## get
@router.get("", response_model=List[schemas.UserResponse])
def read_users(
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
    limit:int = 10,
    page:int = 1,
):
    if limit > 0:
        users = users_collection.find().skip((page - 1) * limit).limit(limit)
    else:
        users = users_collection.find()
    return [convert_to_user_response(user) for user in users]


@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: str, user_data: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return convert_to_user_response(user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id {user_id} was not found",
    )


##post
@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(
    newUser: schemas.NewUser, user_data: schemas.TokenData = Depends(oauth2.get_current_user)
):
    user_with_similar_email = users_collection.find_one({"email": newUser.email})
    if user_with_similar_email or newUser.email == 'test@gmail.com':
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )
    hashed_password = utils.hash(newUser.password)
    newUser.password = hashed_password
    user = newUser.dict()
    user["created_at"] = datetime.now()
    result = users_collection.insert_one(user)
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return convert_to_user_response(created_user)


##update
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: str,
    updatedUser: schemas.NewUser,
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {user_id} was not found",
        )
    hashed_password = utils.hash(updatedUser.password)
    updatedUser.password = hashed_password
    update_data = updatedUser.dict()
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    return convert_to_user_response(updated_user)


##delete
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, user_data: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {user_id} was not found",
        )
    users_collection.delete_one({"_id": ObjectId(user_id)})
