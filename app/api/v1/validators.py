from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tables import personal_tables_crud
from app.crud.reservation import reservation_crud
from app.models import Reservation, PersonalTable, User


async def check_name_duplication(table_name: str, session: AsyncSession) -> None:
    table_id = await personal_tables_crud.get_table_id_by_name(table_name, session)
    if table_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Стол с таким именем уже существует!'
        )


async def check_personal_table_exists(table_id: int, session: AsyncSession) -> PersonalTable:
    personal_table = await personal_tables_crud.get(table_id, session)
    if personal_table is None:
        raise HTTPException(status_code=404,
                            detail='Стол не найден!')
    return personal_table


async def check_reservation_intersections(**kwargs) -> None:
    reservations = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if reservations:
        raise HTTPException(status_code=422, detail=str(reservations))


async def check_reservation_before_edit(
        reservation_id: int,
        session: AsyncSession,
        user: User
) -> Reservation:
    reservation = await reservation_crud.get(
        obj_id=reservation_id, session=session
    )
    if not reservation:
        raise HTTPException(status_code=404, detail='Бронь не найдена!')
    if reservation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно удалить или редактировать чужую бронь!'
        )
    return reservation
