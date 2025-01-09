from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import delete

from brainagriculturetest.src.ports.outbound.database.models import Farm

class OutboundFarmRepositoryPort():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_farm(self, farmer_id: int, farm_data: dict) -> Farm:
        farm = Farm(
            name=farm_data["name"],
            arable_area=farm_data["arable_area"],
            vegetation_area=farm_data["vegetation_area"],
            total_area=farm_data["total_area"],
            farmer_id=farmer_id,
        )
        self.session.add(farm)
        await self.session.commit()
        await self.session.refresh(farm)
        return farm
    
    async def delete_farm(self, farm_id: int):
        await self.session.execute(
            delete(Farm)
            .where(Farm.id == farm_id)
        )
        await self.session.commit()