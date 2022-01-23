"""
FastAPI testing
"""

import os
import time

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models, schemas, utils
from .config import settings
from .database import engine
from .routers import post, user

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


# Include router objects from routers directory
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    """
    Root path
    """
    return {"message": "welcome to my api!!"}