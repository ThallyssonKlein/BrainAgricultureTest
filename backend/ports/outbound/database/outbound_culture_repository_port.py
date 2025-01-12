from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update

from ports.outbound.database.models import Culture

class OutboundCultureRepositoryPort:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def delete_culture(self, culture_id: int):
        try:
            await self.session.execute(
            delete(Culture)
                .where(Culture.id == culture_id)
            )
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def create_culture_for_a_farmer(self, farmer_id: int, culture: dict):
        stmt = (
            insert(Culture)
            .values(**culture, farmer_id=farmer_id)
            .returning(Culture)
        )

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()

            created_culture = result.scalars().first()
            return created_culture
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_cultures_for_a_farmer(self, farmer_id: int):
        try:
            result = await self.session.execute(select(Culture).where(Culture.farmer_id == farmer_id))
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def get_by_farmer_id_and_name(self, farmer_id: int, culture_name: str):
        try:
            result = await self.session.execute(select(Culture).where(Culture.farmer_id == farmer_id, Culture.name == culture_name).limit(1))
            return result.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def update_culture_by_id(self, culture_id: int, culture: dict):
        try:
            stmt = (
                update(Culture)
                .where(Culture.id == culture_id)
                .values(**culture)
                .returning(Culture)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_culture = result.scalars().first()

            if not updated_culture:
                raise ValueError("Culture not found.")

            return updated_culture
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_culture_by_id(self, culture_id: int):
        try:
            result = await self.session.execute(
                delete(Culture).where(Culture.id == culture_id)
            )
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            raise e
