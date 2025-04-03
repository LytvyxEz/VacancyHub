from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    if not password or password is None:
        raise Exception

    hashed_password = pwd_context.hash(password)

    return hashed_password

