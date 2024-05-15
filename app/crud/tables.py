from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.tables import PersonalTable


class CrudPersonalTables(CRUDBase):

    async def get_table_id_by_name(self,
                                   table_name: str,
                                   session: AsyncSession) \
            -> Optional[int]:
        db_table_id = await session.execute(select(PersonalTable.id).where(PersonalTable.name == table_name))
        db_table_id = db_table_id.scalars().first()
        return db_table_id


personal_tables_crud = CrudPersonalTables(PersonalTable)
