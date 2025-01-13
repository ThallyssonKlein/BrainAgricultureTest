from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update

from ports.outbound.database.models import Culture
from shared.loggable import Loggable

class OutboundCultureRepositoryPort(Loggable):
    def __init__(self, session: AsyncSession):
        Loggable.__init__(self, prefix="OutboundCultureRepositoryPort")
        self.session = session
    
    async def delete_culture(self, culture_id: int, trace_id: str):
        try:
            await self.session.execute(
            delete(Culture)
                .where(Culture.id == culture_id)
            )
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error deleting culture: {e}", trace_id)
            raise e
    
    async def create_culture_for_a_farmer(self, farmer_id: int, culture: dict, trace_id: str):
        try:
            stmt = (
                insert(Culture)
                .values(**culture, farmer_id=farmer_id)
                .returning(Culture)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            created_culture = result.scalars().first()
            return created_culture
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error creating culture: {e}", trace_id)
            raise e
    
    async def get_cultures_for_a_farmer(self, farmer_id: int, trace_id: str):
        try:
            result = await self.session.execute(select(Culture).where(Culture.farmer_id == farmer_id))
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error getting cultures: {e}", trace_id)
            raise e
    
    async def get_by_farmer_id_and_name(self, farmer_id: int, culture_name: str, trace_id: str):
        try:
            result = await self.session.execute(select(Culture).where(Culture.farmer_id == farmer_id, Culture.name == culture_name).limit(1))
            return result.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error getting culture: {e}", trace_id)
            raise e
    
    async def update_culture_by_id(self, culture_id: int, culture: dict, trace_id: str):
        try:
            stmt = (
                update(Culture)
                .where(Culture.id == culture_id)
                .values(name=culture["name"])
                .returning(Culture)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_culture = result.scalars().first()

            if not updated_culture:
                raise ValueError("Culture not found")

            return updated_culture
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error updating culture: {e}", trace_id)
            raise e

    async def delete_culture_by_id(self, culture_id: int, trace_id: str):
        try:
            result = await self.session.execute(
                delete(Culture).where(Culture.id == culture_id)
            )
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error deleting culture: {e}", trace_id)
            raise e
    
    async def find_culture_by_id(self, culture_id: int, trace_id: str):
        try:
            result = await self.session.execute(select(Culture).where(Culture.id == culture_id).limit(1))
            return result.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding culture: {e}", trace_id)
            raise e
