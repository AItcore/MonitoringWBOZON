from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from Database.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, record_id: int):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(id=record_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                print(f"Error fetching {cls.model.__name__} with ID {record_id}: {e}")
                return None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            try:
                query = select(cls.model)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                print(f"Error fetching all {cls.model.__name__}: {e}")
                return None

    @classmethod
    async def create(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                new_record = cls.model(**kwargs)
                session.add(new_record)
                await session.commit()
                return new_record
            except SQLAlchemyError as e:
                print(f"Error creating {cls.model.__name__}: {e}")
                return None

    @classmethod
    async def delete_by_id(cls, record_id: int):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(id=record_id)
                result = await session.execute(query)
                record = result.scalar_one_or_none()
                if record:
                    await session.delete(record)
                    await session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                print(f"Error deleting {cls.model.__name__} with ID {record_id}: {e}")
                return False

