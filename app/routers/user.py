"""
User info functions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users")


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    New user registration
    """
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Automatically unpack all dict fields
    new_user = models.User(**user.dict())

    # Add new post to the database
    db.add(new_user)

    # Commit new row to the database
    db.commit()

    # Retrive new post and store in new_user variable
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
