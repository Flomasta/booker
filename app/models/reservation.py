from sqlalchemy import Column, DateTime, ForeignKey, Integer
from app.core.database import Base


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    personal_table_id = Column(Integer, ForeignKey('personaltable.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
