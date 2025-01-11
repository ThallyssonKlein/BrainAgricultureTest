from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import delete

from ports.outbound.database.models import Crop, Farm, Farmer

class OutboundFarmerRepositoryPort():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_farmer(self, farmer_data: dict):
        farmer = Farmer(
            document=farmer_data["document"],
            name=farmer_data["name"],
            city=farmer_data["city"],
            state=farmer_data["state"],
        )
        self.session.add(farmer)
        await self.session.commit()
        await self.session.refresh(farmer)
        return farmer

    async def delete_farmer(self, farmer_id: int):
        await self.session.execute(
            delete(Farmer)
            .where(Farmer.id == farmer_id)
        )
        await self.session.commit()
    
    async def find_farmers_paginated_and_with_query(self, limit: int, offset: int, query: str):
        stmt = select(Farmer).offset(offset - 1).limit(limit).options(
            selectinload(Farmer.farms).selectinload(Farm.crops).selectinload(Crop.culture)
        )
        
        if query:
            stmt = stmt.where(Farmer.name.ilike(f"%{query}%"))

        result = await self.session.execute(stmt)
        return result.scalars().all()
