from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "06f48b26d62f0473bd9594a11ebcc73772dac1d732850966ca8cc6618b239039"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    # Data will be encoded with the JWT token
    # Copy data so we don't change the original
    to_encode = data.copy()

    # Grab the current time and add ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify that the access token is valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Calls the verify_access_token function
    """
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail=f'{"Could not validate credentials"}',
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)