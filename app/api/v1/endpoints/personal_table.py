from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tables import personal_tables_crud
from app.schemas.tables import PersonalTableCreate, PersonalTableDB, PersonalTableUpdate
from app.core.database import get_async_session
from app.api.v1.validators import check_personal_table_exists, check_name_duplication
from app.core.user import current_superuser

router = APIRouter()


@router.post('/', response_model=PersonalTableDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)], )
async def create_new_personal_table(
        personal_table: PersonalTableCreate,
        session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров."""
    await check_name_duplication(personal_table.name, session)
    new_table = await personal_tables_crud.create(personal_table, session)
    return new_table


@router.get('/', response_model=list[PersonalTableDB], response_model_exclude_none=True)
async def get_all_tables(session: AsyncSession = Depends(get_async_session)):
    tables = await personal_tables_crud.get_all(session)
    return tables


@router.patch(
    '/{table_id}',
    response_model=PersonalTableDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def partially_update_personal_table(
        personal_table_id: int,
        obj_in: PersonalTableUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    personal_table = await check_personal_table_exists(personal_table_id, session)
    if obj_in.name is not None:
        await check_name_duplication(obj_in.name, session)
    personal_table = await personal_tables_crud.update(personal_table, obj_in, session)
    return personal_table


@router.delete(
    '/{personal_table_id}',
    response_model=PersonalTableDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def remove_personal_table(personal_table_id: int, session: AsyncSession = Depends(get_async_session)):
    personal_table = await check_personal_table_exists(personal_table_id, session)
    personal_table = await personal_tables_crud.remove(personal_table, session)
    return personal_table
