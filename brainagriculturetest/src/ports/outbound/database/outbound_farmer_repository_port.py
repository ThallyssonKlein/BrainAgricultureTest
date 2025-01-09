from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select, delete

from brainagriculturetest.src.ports.outbound.database.models import Crop, Farm, Farmer

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

    async def get_farm_relations(self, farmer_id: int):
        result = await self.session.execute(
            select(Farmer)
            .where(Farmer.id == farmer_id)
            .options(
                selectinload(Farmer.farms).selectinload(Farm.crops).selectinload(Crop.culture)
            )
        )
        farmer_with_relations = result.scalar_one()

        return farmer_with_relations

    async def delete_farmer(self, farmer_id: int):
        await self.session.execute(
            delete(Farmer)
            .where(Farmer.id == farmer_id)
        )
        await self.session.commit()