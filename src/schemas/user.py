from pydantic import BaseModel, EmailStr, Field, field_validator, PositiveInt, constr
from string import punctuation
from fastapi import HTTPException
from src.utils import hash_password


speacial_chars = punctuation


class User(BaseModel):
    _id: PositiveInt
    email: EmailStr = Field(max_length=256)
    password: constr(min_length=8, max_length=64)


    @field_validator("password")
    def check_password(cls, value):

        if not any(char.isalpha() for char in value):
            raise HTTPException(400, "Password must have at least one uppercase letter")


        if not any(char.isupper() for char in value):
            raise HTTPException(400, "Password must have at least one uppercase letter")

        if not any(char.islower() for char in value):
            raise HTTPException(400, "Password must have at least one lowercase letter")

        if not any(char.isdigit() for char in value):
            raise HTTPException(400, "Password must have at least one digit")

        if not any(char in speacial_chars for char in value):
            raise HTTPException(400, "Password must have at least one special symbol")

        return value


    @field_validator('password')
    def hash_password(cls, value):

        password = hash_password(value)

        return password
