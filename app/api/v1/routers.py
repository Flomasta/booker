from fastapi import APIRouter

from app.api.v1.endpoints import personal_table_router, reservation_router,user_router

main_router = APIRouter()
main_router.include_router(personal_table_router, prefix='/personal_table', tags=['Personal tables'])
main_router.include_router(reservation_router, prefix='/reservations', tags=['Reservations'])
main_router.include_router(user_router)
