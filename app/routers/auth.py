from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """
    User login route
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    # Provide a minimal amount of info for bad login attempts. This ensures
    # that we don't send info to an attacker about whether the email or
    # password was invalid.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{"Invalid Credentials"}'
        )

    # Fail if the user-provided JWT signature doesn't match our signature
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='{"Invalid Credentials"}'
        )

    return {"token": "example token"}