from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

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
        try:
            await self.session.commit()
            await self.session.refresh(farmer)
            return farmer
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Farmer with this document already exists") from e


    async def update_farmer(self, farmer_data: dict):
        stmt = select(Farmer).where(Farmer.id == farmer_data['id'])
        result = await self.session.execute(stmt)
        farmer = result.scalars().first()

        if not farmer:
            raise ValueError("Farmer not found with the provided id")

        # Atualizar os campos
        farmer.name = farmer_data.get("name", farmer.name)
        farmer.city = farmer_data.get("city", farmer.city)
        farmer.state = farmer_data.get("state", farmer.state)

        try:
            await self.session.commit()
            await self.session.refresh(farmer)
            return farmer
        except IntegrityError as e:
            await self.session.rollback()
            raise e


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
    
    async def delete_farmer_by_id(self, farmer_id: int):
        await self.session.execute(
            delete(Farmer)
            .where(Farmer.id == farmer_id)
        )
        await self.session.commit()