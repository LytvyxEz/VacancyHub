from pydantic import BaseModel, EmailStr, Field, field_validator, PositiveInt
from string import punctuation
from fastapi import HTTPException

speacial_chars = punctuation

class User(BaseModel):
    _id: PositiveInt
    email: EmailStr = Field(max_length=256)
    password: constr(min_length=8, max_length=20)


    @field_validator("password")
    def check_password(cls, value):

        if not any(i.isupper() for i in value):
            raise HTTPException(400, "Password must have at least one uppercase letter")

        if not any(i.islower() for i in value):
            raise HTTPException(400, "Password must have at least one lowercase letter")

        if not any(i.isdigit() for i in value):
            raise HTTPException(400, "Password must have at least one digit")

        if not any(char in special_chars for char in password):
            raise HTTPException(400, "Password must have at least one special symbol")

        return value
