from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str):
    if not password or password is None:
        raise Exception

    hashed_password = generate_password_hash(password)

    return hashed_password

