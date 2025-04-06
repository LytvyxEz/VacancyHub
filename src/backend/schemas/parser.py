from pydantic import BaseModel, Field

class ParserRequest(BaseModel):
    query: str = Field(
        default="Python",
        description="Пошуковий запит для вакансій",
        min_length=2,
        max_length=100
    )
    analyze_description: bool = Field(
        default=True,
        description="Аналізувати повний опис вакансії на наявність навичок"
    )