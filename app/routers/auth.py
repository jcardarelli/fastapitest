from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    User login route
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    # Provide a minimal amount of info for bad login attempts. This ensures
    # that we don't send info to an attacker about whether the email or
    # password was invalid.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'{"Invalid Credentials"}'
        )

    # Fail if the user-provided JWT signature doesn't match our signature
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='{"Invalid Credentials"}'
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}