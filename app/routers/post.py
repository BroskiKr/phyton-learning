from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List
from app import models, schemas, oauth2
from app.postgres_db import get_db
from sqlalchemy.orm import Session
from app.mongo_db import users_collection
from bson import ObjectId


router = APIRouter(prefix="/posts", tags=["Posts"])


## get
@router.get("", response_model=List[schemas.PostResponse])
def read_posts(
    response: Response,
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db),
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    user = users_collection.find_one({"_id": ObjectId(user_data.id)})
    if user["email"] == "admin@gmail.com":
        total_count = db.query(models.Post).count()
        if limit > 0:
            posts = (
                db.query(models.Post)
                .order_by(models.Post.id.desc())
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )
        else:
            posts = db.query(models.Post).order_by(models.Post.id.desc()).all()
    else:
        total_count = (
            db.query(models.Post).filter(models.Post.owner_id == user_data.id).count()
        )
        if limit > 0:
            posts = (
                db.query(models.Post)
                .filter(models.Post.owner_id == user_data.id)
                .order_by(models.Post.id.desc())
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )
        else:
            posts = (
                db.query(models.Post)
                .filter(models.Post.owner_id == user_data.id)
                .order_by(models.Post.id.desc())
                .all()
            )

    response.headers["X-Total-Count"] = str(total_count)
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def read_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    user = users_collection.find_one({"_id": ObjectId(user_data.id)})
    if user["email"] == "admin@gmail.com":
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
    else:
        post = (
            db.query(models.Post)
            .filter(models.Post.id == post_id, models.Post.owner_id == user_data.id)
            .first()
        )
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {post_id} was not found",
    )


##post
@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    newPost: schemas.NewPost,
    db: Session = Depends(get_db),
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    newPost.owner_id = user_data.id
    post = models.Post(**newPost.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


##update
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    updatedPost: schemas.UpdatePost,
    db: Session = Depends(get_db),
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    user = users_collection.find_one({"_id": ObjectId(user_data.id)})
    if user["email"] == "admin@gmail.com":
        post_query = db.query(models.Post).filter(models.Post.id == post_id)
    else:
        post_query = db.query(models.Post).filter(
            models.Post.id == post_id, models.Post.owner_id == user_data.id
        )
    post = post_query.first()
    if post:
        if not updatedPost.title:
            updatedPost.title = post.title
        if not updatedPost.body:
            updatedPost.body = post.body
        post_query.update(updatedPost.dict(), synchronize_session=False)
        db.commit()
        db.refresh(post)
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {post_id} was not found",
    )


##delete
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    user = users_collection.find_one({"_id": ObjectId(user_data.id)})
    if user["email"] == "admin@gmail.com":
        post = db.query(models.Post).filter(models.Post.id == post_id)
    else:
        post = db.query(models.Post).filter(
            models.Post.id == post_id, models.Post.owner_id == user_data.id
        )
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} was not found",
        )
    post.delete(synchronize_session=False)
    db.commit()
