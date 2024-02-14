from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    category: str = Field(...)
