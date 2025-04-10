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
    def encode_jwt(email: EmailStr, token_type: str, expire_time: int = 30):
        payload = {
            'sub': email,
            'exp': datetime.utcnow() + timedelta(minutes=expire_time),
            'iat': datetime.utcnow(),
            'typ': token_type
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=TOKEN_ALG)

    @staticmethod
    def decode_jwt(token: str):
        return jwt.decode(token.replace("Bearer", ""), key=SECRET_KEY, algorithms=[TOKEN_ALG])

    @classmethod
    def create_tokens(cls, email: EmailStr):
        access_token = cls.encode_jwt(email, token_type="access", expire_time=60 * 24)
        refresh_token = cls.encode_jwt(email, token_type="refresh", expire_time=60 * 24 * 7)

        print(f"access - {access_token}\nrefresh - {refresh_token}")
        return {"access_token": access_token,
                "refresh_token": refresh_token}

