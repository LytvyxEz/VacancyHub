import jwt
from pydantic import EmailStr
from datetime import datetime, timedelta
import dotenv
import os

dotenv.load_dotenv()

TOKEN_ALG = os.getenv("TOKEN_ALG")
SECRET_KEY = os.getenv("SECRET_KEY")


class JWT:
    @staticmethod
    def encode_jwt(email: EmailStr):
        utc_now = datetime.utcnow()
        payload = {
            'sub': email,
            'exp': utc_now + timedelta(minutes=10),
            'iat': utc_now,
            'type': 'ACCESS_TOKEN_TYPE'
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=TOKEN_ALG)

    @staticmethod
    def decode_jwt(token: str):
        return jwt.decode(token, key=SECRET_KEY, algorithms=[TOKEN_ALG])

