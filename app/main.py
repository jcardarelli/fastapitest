"""
FastAPI testing
"""

import os

from fastapi import FastAPI

from .routers import auth, post, user, vote

app = FastAPI()

# Get env vars
path = os.getenv("POSTGRES_CONNECTION")


# Include router objects from routers directory
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    """
    Root path
    """
    return {"message": "welcome to my api!!"}
