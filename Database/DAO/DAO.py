from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from Database.database import async_session_maker
from Database.DAO.base import BaseDAO
from Database.models import *

class PlaceHistoryDAO(BaseDAO):
    model = PlaceHistory
    
    @classmethod
    async def bulk_create(cls, records: list[dict]):
        async with async_session_maker() as session:
            try:
                await session.execute(insert(cls.model).values(records))
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"Bulk insert error: {e}")
                return False
    
class CardsDAO(BaseDAO):
    model = Cards