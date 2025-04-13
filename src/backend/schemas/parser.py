from pydantic import BaseModel, Field, PositiveInt, model_validator, field_validator
from fastapi import Request, HTTPException
from typing import Optional


class ParserRequest(BaseModel):
    query: Optional[str] = Field(min_length=1, max_length=30)
    experience: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    salary: Optional[PositiveInt] = Field(None)

    @field_validator('salary')
    def validate_salary(cls, v):
        if v == "":
            v = None
            return v

        return v


    @model_validator(mode='before')
    def request_validator(cls, values):
        for i in ['experience', 'location', 'salary']:
            if i in values and (values[i] == '' or values[i] is None):
                values[i] = None
        return values


def query_validator(query):
    if not query or query == '':
        raise ValueError('Query is required')

    return query