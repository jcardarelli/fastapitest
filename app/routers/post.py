"""
Post functions
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """
    Get all posts
    """
    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
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
@router.get("/{post_id}", response_model=schemas.PostResponse)
# using '(post_id: int) will tell fastapi to auto-convert to an integer
def get_post(post_id: int, db: Session = Depends(get_db)):
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


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
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
