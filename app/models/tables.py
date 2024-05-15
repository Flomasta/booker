from sqlalchemy import Column, String, Text
from app.core.database import Base
from sqlalchemy.orm import relationship


class PersonalTable(Base):
    name = Column(String(150), unique=True, nullable=False)
    comment = Column(Text)
    description = Column(Text)
    reservations = relationship('Reservation',cascade='delete')
