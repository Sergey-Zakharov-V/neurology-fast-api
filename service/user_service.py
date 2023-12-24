from models.users import Users, Payments
from service.base import BaseService
from sqlalchemy import select, insert, delete, and_, update

from database import async_session_maker


class UserService(BaseService):
    model = Users

    @classmethod
    async def update_key(cls, username: str, key: str):
        async with async_session_maker() as session:
            await session.execute(
                update(cls.model).where(cls.model.username == username).values(key=key)
            )
            await session.commit()

    @classmethod
    async def update(cls, username: str, value: int):
        async with async_session_maker() as session:
            current_quantity = await session.execute(
                select(cls.model.transcripts).where(cls.model.username == username)
            )
            transcripts_value = current_quantity.scalar()
            await session.execute(
                update(cls.model).where(cls.model.username == username).values(transcripts=transcripts_value + value)
            )
            await session.commit()

    @classmethod
    async def update_transcripts(cls, key: str, value: int):
        async with async_session_maker() as session:
            print(key)
            current_quantity = await session.execute(
                select(cls.model.transcripts).where(cls.model.key == key)
            )
            transcripts_value = current_quantity.scalar()
            if type(current_quantity) is int:
                await session.execute(
                    update(cls.model).where(cls.model.key == key).values(transcripts=transcripts_value + value)
                )
                await session.commit()


class PaymentService(BaseService):
    model = Payments

    @classmethod
    async def update(cls, key: str, status: str):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Users.username).where(Users.key == key)
            )
            username = result.scalar()
            await session.execute(
                update(cls.model).where(cls.model.username == username).values(status=status)
            )
            await session.commit()
