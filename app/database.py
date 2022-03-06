from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQL_ALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}"
    f"/{settings.database_name}"
)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class (our models will extend this class)
Base = declarative_base()


def get_db():
    """
    nicely close database connections
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
