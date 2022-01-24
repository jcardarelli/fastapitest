from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """
    Verify that the user's plain password matches the hashed password we have
    on file
    """
    return pwd_context.verify(plain_password, hashed_password)
