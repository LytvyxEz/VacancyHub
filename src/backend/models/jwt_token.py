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
            'iat': utc_now,
            'type': 'ACCESS_TOKEN_TYPE'
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=TOKEN_ALG)

    @staticmethod
    def decode_jwt(token: str):
        return jwt.decode(token.split()[1], key=SECRET_KEY, algorithms=[TOKEN_ALG])

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALG])
            return payload["sub"]
        except Exception as e:
            return None
