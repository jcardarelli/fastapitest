"""
FastAPI testing
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, post, user, vote

app = FastAPI()

# CORS setup, runs before every request
origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
