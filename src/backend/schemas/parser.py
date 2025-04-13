from pydantic import BaseModel, Field, PositiveInt, model_validator, field_validator
from fastapi import Request, HTTPException
from typing import Optional


class ParserRequest(BaseModel):
    query: Optional[str] = Field(min_length=1, max_length=30)
    experience: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    salary: Optional[int] = Field(default=0, ge=0)
    max_pages: Optional[PositiveInt] = Field(default=20)

    @field_validator("location")
    def ensure_utf8(cls, value):
        if value is not None and isinstance(value, str):
            return value.encode("utf-8").decode("utf-8")
        return value


    @field_validator('salary')
    def validate_salary(cls, v):
        if v == "":
            v = 0
            return v

        return v

    @model_validator(mode='before')
    def request_validator(cls, values):
        for i in ['experience', 'location']:
            if i in values and (values[i] == '' or values[i] is None):
                values[i] = None
        return values

    @field_validator('max_pages')
    def validate_max_pages(cls, v):
        if v == "" or v == "None":
            return 20
        try:
            return int(v)
        except (ValueError, TypeError):
            return 20

def parser_request(request: Request, query, experience, location, salary, max_pages):
    parser_request = ParserRequest(
        query=query,
        experience=experience,
        location=location,
        salary=salary,
        max_pages=max_pages
    )

    query = parser_request.query
    experience = parser_request.experience
    location = parser_request.location
    salary = parser_request.salary
    max_pages = parser_request.max_pages

    parser_query = {
        'query': query,
        'experience': experience,
        'location': location,
        'salary': salary,
        'max_pages': max_pages,
        'url_query': request.url.query
    }

    return parser_query
