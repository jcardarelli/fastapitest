"""
Schema definitions
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    """
    Set schema from base model
    """

    # Required inputs
    title: str
    content: str

    # Optional inputs
    published: bool = True


class PostCreate(PostBase):
    """
    Set schema for creating posts
    """

    # Accept anything from the base class
    pass


class PostResponse(PostBase):
    """
    Allowed fields in the response to the user
    """

    id: int
    created_at: datetime

    # Tell the pydantic model to read the data even if it is not a dict
    # Get value from dict, e.g. id = data["id"]
    # Get value from attribute, e.g. id = data.id
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Fields required to create a new user account
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Fields to return to the user when they create an account
    """

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """
    docstring for UserLogin class
    """

    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
