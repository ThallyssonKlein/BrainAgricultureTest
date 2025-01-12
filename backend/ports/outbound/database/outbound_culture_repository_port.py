from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update

from ports.outbound.database.models import Culture

class OutboundCultureRepositoryPort:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_culture(self, culture_name: str) -> Culture:
        result = await self.session.execute(select(Culture).where(Culture.name == culture_name))
        culture = result.scalar_one_or_none()
        if not culture:
            culture = Culture(name=culture_name)
            self.session.add(culture)
            await self.session.commit()
            await self.session.refresh(culture)
        return culture
    
    async def delete_culture(self, culture_id: int):
        await self.session.execute(
            delete(Culture)
            .where(Culture.id == culture_id)
        )
        await self.session.commit()
    
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
        result = await self.session.execute(select(Culture).where(Culture.farmer_id == farmer_id))
        return result.scalars().all()
    
    async def get_by_farmer_id_and_name(self, farmer_id: int, culture_name: str):
        result = await self.session.execute(select(Culture).where(Culture.farmer_id == farmer_id, Culture.name == culture_name).limit(1))
        return result.scalar_one_or_none()
    
    async def update_culture_by_id(self, culture_id: int, culture: dict):
        d = culture.model_dump()
        await self.session.execute(
            update(Culture)
            .where(Culture.id == culture_id)
            .values(**d)
        )
        await self.session.commit()
        result = await self.session.execute(select(Culture).where(Culture.id == culture_id))
        return result.scalar_one()

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
