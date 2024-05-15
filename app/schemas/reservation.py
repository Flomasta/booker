from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator, model_validator, Extra, Field
from typing import Optional

FROM_TIME = (
        datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
        datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class ReservationCreate(ReservationBase):
    personal_table_id: int


class ReservationUpdate(ReservationBase):
    @field_validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError('Время начала бронирования не может быть '
                             'раньше текущей даты')
        return value

    @model_validator(mode='before')
    def check_to_reserve_later_than_from_reserve(cls, values):
        if values['to_reserve'] <= values['from_reserve']:
            raise ValueError('Время окончания бронирования '
                             'не может быть'
                             'меньше даты начала бронирования')
        return values


class ReservationDB(ReservationBase):
    id: int
    personal_table_id: int
    user_id: Optional[int]

    class Config:
        from_orm = True
