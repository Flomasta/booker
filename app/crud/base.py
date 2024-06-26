from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, List, Optional, Type, TypeVar
from app.core.database import Base
from pydantic import BaseModel

from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self,
                  obj_id: int,
                  session: AsyncSession
                  ) -> Optional[ModelType]:
        db_obj = await session.execute(select(self.model).where(self.model.id == obj_id))
        return db_obj.scalars().first()

    async def get_all(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self,
                     obj_to_create: CreateSchemaType,
                     session: AsyncSession,
                     user: Optional[User] = None) -> ModelType:
        obj_to_create_data = obj_to_create.model_dump()
        if user:
            obj_to_create_data['user_id'] = user.id
        db_obj = self.model(**obj_to_create_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: UpdateSchemaType, session: AsyncSession) -> ModelType:
        db_obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in db_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: ModelType, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
