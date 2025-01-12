from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, insert, update
from sqlalchemy.exc import IntegrityError

from ports.outbound.database.models import Farmer

class OutboundFarmerRepositoryPort():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_farmer(self, farmer_data: dict):
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

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()

            created_farmer = result.scalars().first()
            return created_farmer
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Farmer with this document already exists") from e
        except Exception as e:
            await self.session.rollback()
            raise e



    async def update_farmer(self, farmer_data: dict):
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

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_farmer = result.scalars().first()

            if not updated_farmer:
                raise ValueError("Farmer not found with the provided id")

            return updated_farmer
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def find_farmers_paginated_and_with_query(self, limit: int, offset: int, query: str):
        try:
            stmt = select(Farmer).offset(offset - 1).limit(limit)
        
            if query:
                stmt = stmt.where(Farmer.name.ilike(f"%{query}%"))

            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def delete_farmer_by_id(self, farmer_id: int):
        try:
            result = await self.session.execute(
                delete(Farmer).where(Farmer.id == farmer_id)
            )
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            raise e
