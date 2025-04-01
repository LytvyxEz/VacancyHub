from pydantic import BaseModel, EmailStr, Field, field_validator
from string import punctuation
from typing import Annotated
from fastapi import HTTPException
from src.utils import hash_password

special_chars = punctuation


class User(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str

    @field_validator('password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise HTTPException(400, "Password must have at least one uppercase letter")

        if not any(char.isupper() for char in value):
            raise HTTPException(400, "Password must have at least one uppercase letter")

        if not any(char.islower() for char in value):
            raise HTTPException(400, "Password must have at least one lowercase letter")

        if not any(char.isdigit() for char in value):
            raise HTTPException(400, "Password must have at least one digit")

        if not any(char in special_chars for char in value):
            raise HTTPException(400, "Password must have at least one special symbol")

        return value

    @field_validator('confirm_password')
    def validate_confirm_password(cls, value: str, values):
        if 'password' in values.data and value != values.data['password']:
            raise HTTPException(400, "Passwords don't match")
        return value


class UserInDB(User):
    hashed_password: User

    @classmethod
    def create_from_user(cls, user_create: User):
        return cls(
            email=user_create.email,
            hashed_password=hash_password(user_create.password)
        )