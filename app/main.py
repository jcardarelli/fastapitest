"""
FastAPI testing
"""

import os
import time
from typing import List

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas
from .config import settings
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Get env vars
path = os.getenv("POSTGRES_CONNECTION")
print(path)

# Setup database connection
while True:
    try:
        conn = psycopg2.connect(
            host=settings.database_hostname,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            # Sets up python dict with column name and value
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")

        # break out of while loop if true
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)

        # wait before reconnecting
        time.sleep(2)

my_posts = [
    {"title": "post title 1", "content 1": "content of post 1", "post_id": 1},
    {"title": "post title 2", "content 2": "content of post 2", "post_id": 2},
]


def find_post(post_id):
    """
    Retrieve data for a single post
    """
    for post in my_posts:
        if post["post_id"] == post_id:
            return post


def find_index_post(post_id):
    """
    Find the index integer of a post in the array
    """
    for index, post in enumerate(my_posts):
        if post["post_id"] == post_id:
            return index


@app.get("/")
def root():
    """
    Root path
    """
    return {"message": "welcome to my api!!"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """
    Get all posts
    """
    posts = db.query(models.Post).all()
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a post
    """
    # Automatically unpack all dict fields
    new_post = models.Post(**post.dict())

    # Add new post to the database
    db.add(new_post)

    # Commit new row to the database
    db.commit()

    # Retrive new post and store in new_post variable
    db.refresh(new_post)

    return new_post


# path parameter {post_id}
@app.get("/posts/{post_id}")
# using '(post_id: int) will tell fastapi to auto-convert to an integer
def get_post(
    post_id: int, db: Session = Depends(get_db), response_model=schemas.PostResponse
):
    """
    Get a single post
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} was not found",
        )

    return {"post_detail": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a single post
    """
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} does not exist",
        )

    post.delete(synchronize_session=False)
    db.commit()

    # Don't send any data back when deleting
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    response_model=schemas.PostResponse,
):
    """
    Update a post
    """
    # query to find post with specific id
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    # grab the post with that id
    post = post_query.first()

    # return 404 if it doesn't exist
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} does not exist",
        )

    # if it does exist, chain the update method to the same query method
    post_query.update(updated_post.dict(), synchronize_session=False)

    # commit changes to database
    db.commit()

    # send updated post to user
    return post_query.first()


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    New user registration
    """
    # Automatically unpack all dict fields
    new_user = models.User(**user.dict())

    # Add new post to the database
    db.add(new_user)

    # Commit new row to the database
    db.commit()

    # Retrive new post and store in new_user variable
    db.refresh(new_user)

    return new_user