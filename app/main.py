"""
FastAPI testing
"""

from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    """
    Valpost_idate schema with pydantic
    """

    # Required inputs
    title: str
    content: str

    # Optional inputs
    published: bool = True
    rating: Optional[int] = None


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


@app.get("/posts")
def get_posts():
    """
    Get all posts
    """
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    Create a post
    """
    post_dict = post.dict()
    post_dict["post_id"] = randrange(0, 10000000)

    my_posts.append(post_dict)
    return {"data": post_dict}


# path parameter {post_id}
@app.get("/posts/{post_id}")
# using '(post_id: int) will tell fastapi to auto-convert to an integer
def get_post(post_id: int):
    """
    Get a single post
    """
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {post_id} was not found"}

    return {"post_detail": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """
    Delete a single post
    """
    # find index in array that has the ID we're looking for
    # my_posts.pop(index)
    index = find_index_post(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} does not exist",
        )

    # Remove from array
    my_posts.pop(index)

    # Don't send any data back when deleting
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    """
    Update a post
    """
    # find index in array that has the ID we're looking for
    index = find_index_post(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {post_id} does not exist",
        )

    # Convert input data into a dictionary
    post_dict = post.dict()

    # Add id to the dict
    post_dict["post_id"] = post_id

    # Update this index
    my_posts[index] = post_dict

    return {"data": post_dict}