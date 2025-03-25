from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):

    if not password or password is None:
        raise Exception

    hash_password = generate_password_hash(password)

    return hash_password

