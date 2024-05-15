"""Импорты класса Base и всех моделей для Alembic.
Чтобы IDE не ругалась на неиспользуемые импорты noqa (NO Quality Assurance)
"""
from app.core.database import Base  # noqa
from app.models.tables import PersonalTable  # noqa
from app.models.reservation import Reservation  # noqa
from app.models.user import User  # noqa
