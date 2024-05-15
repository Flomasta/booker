from typing import Optional
from pydantic import BaseModel, Field, field_validator
from fastapi import Query


class PersonalTableBase(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    comment: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=3, max_length=200)


class PersonalTable(PersonalTableBase):
    pass


class PersonalTableCreate(PersonalTableBase):
    name: str = Field(min_length=5, max_length=100)


class PersonalTableDB(PersonalTableCreate):
    id: int

    class Config:
        from_orm = True


class PersonalTableUpdate(PersonalTableBase):
    @field_validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название стола не может быть пустым!')
        return value
