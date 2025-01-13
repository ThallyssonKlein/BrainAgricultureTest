from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update
from sqlalchemy.exc import IntegrityError

from ports.outbound.database.models import Farmer
from shared.loggable import Loggable

class OutboundFarmerRepositoryPort(Loggable):
    def __init__(self, session: AsyncSession):
        Loggable.__init__(self, prefix="OutboundFarmerRepositoryPort")
        self.session = session

    async def create_farmer(self, farmer_data: dict, trace_id: str):
        try:
            stmt = (
                insert(Farmer)
                .values(
                    document=farmer_data["document"],
                    name=farmer_data["name"],
                    city=farmer_data["city"],
                    state=farmer_data["state"],
                )
                .returning(Farmer)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            created_farmer = result.scalars().first()
            return created_farmer
        except IntegrityError as e:
            await self.session.rollback()
            self.log.error("Farmer with this document already exists", trace_id)
            raise ValueError("Farmer with this document already exists") from e
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error creating farmer: {e}", trace_id)
            raise e

    async def update_farmer(self, farmer_data: dict, trace_id: str):
        try:
            stmt = (
                update(Farmer)
                .where(Farmer.id == farmer_data["id"])
                .values(
                    document=farmer_data.get("document"),
                    name=farmer_data.get("name"),
                    city=farmer_data.get("city"),
                    state=farmer_data.get("state"),
                )
                .returning(Farmer)
                .execution_options(synchronize_session="fetch")
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_farmer = result.scalars().first()

            if not updated_farmer:
                raise ValueError("Farmer not found with the provided id")

            return updated_farmer
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error updating farmer: {e}", trace_id)
            raise e
    
    async def find_farmers_paginated_and_with_query(self, limit: int, offset: int, query: str, trace_id: str):
        try:
            stmt = select(Farmer).offset(offset - 1).limit(limit)
        
            if query:
                stmt = stmt.where(Farmer.name.ilike(f"%{query}%"))

            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farmers: {e}", trace_id)
            raise e
    
    async def delete_farmer_by_id(self, farmer_id: int, trace_id: str):
        try:
            result = await self.session.execute(
                delete(Farmer).where(Farmer.id == farmer_id)
            )
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error deleting farmer: {e}", trace_id)
            raise e
    
    async def find_farmer_by_id(self, farmer_id: int, trace_id: str):
        try:
            stmt = select(Farmer).where(Farmer.id == farmer_id)
            result = await self.session.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farmer: {e}", trace_id)
            raise e
