from fastapi import APIRouter, Depends
from app.schemas.reservation import ReservationCreate, ReservationDB, ReservationUpdate
from app.core.database import AsyncSessionItem, get_async_session
from app.api.v1.validators import check_personal_table_exists, check_reservation_intersections, \
    check_reservation_before_edit
from app.crud.reservation import reservation_crud

from app.core.user import current_user
from app.models import User

router = APIRouter()


@router.post('/')
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSessionItem = Depends(get_async_session),
        user: User = Depends(current_user)
):
    await check_personal_table_exists(reservation.personal_table_id, session)
    await check_reservation_intersections(**reservation.model_dump(), session=session)
    new_reservation = await reservation_crud.create(reservation, session, user)
    return new_reservation


@router.get('/', response_model=list[ReservationDB])
async def get_all_reservations(
        session: AsyncSessionItem = Depends(get_async_session)
):
    reservations = await reservation_crud.get_all(session)
    return reservations


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB
)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSessionItem = Depends(get_async_session),
        user: User = Depends(current_user)
):
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    reservation = await reservation_crud.remove(
        reservation, session
    )
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSessionItem = Depends(get_async_session),
        user: User = Depends(current_user),
):
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    await check_reservation_intersections(
        **obj_in.model_dump(),
        reservation_id=reservation_id,
        personal_table_id=reservation.personal_table_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=obj_in,
        session=session,
    )
    return reservation


@router.get(
    '/{personal_table_id}/reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'}
)
async def get_reservations_for_personal_table(personal_table_id: int,
                                              session: AsyncSessionItem = Depends(get_async_session)):
    await check_personal_table_exists(table_id=personal_table_id, session=session)
    reservations = await reservation_crud.get_future_reservations_for_table(personal_table_id=personal_table_id,
                                                                            session=session)
    return reservations


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'}
)
async def get_my_reservations(session: AsyncSessionItem = Depends(get_async_session),
                              user: User = Depends(current_user)):
    reservations = await reservation_crud.get_by_user(session=session, user=user)
    return reservations
