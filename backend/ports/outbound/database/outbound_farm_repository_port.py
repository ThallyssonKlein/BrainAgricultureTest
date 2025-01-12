from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, delete, insert, update
from sqlalchemy.orm import selectinload

from adapters.inbound.http.schemas import FarmSchema
from ports.outbound.database.models import Crop, Culture, Farm

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
            city=farm_data["city"],
            state=farm_data["state"]
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

    async def find_farm_counts_grouped_by_state_by_farmer_id(self, farmer_id: int):
        query = select(
            Farm.state,
            func.count(Farm.id).label('farm_count')
        ).where(Farm.farmer_id == farmer_id).group_by(Farm.state)
        result = await self.session.execute(query)
        return result.all()
    
    async def find_farms_count_grouped_by_culture_by_farmer_id(self, farmer_id: int):
        query = select(
            Culture.name,
            func.count(Farm.id).label('farm_count')
        ).join(Crop, Crop.farm_id == Farm.id).join(Culture, Culture.id == Crop.culture_id).where(Farm.farmer_id == farmer_id).group_by(Culture.name)
        
        result = await self.session.execute(query)
        return result.all()
    
    async def find_average_land_use_by_farmer_id(self, farmer_id: int):
        query = select(
            func.coalesce(func.avg(Farm.arable_area), 0).label('average_arable_area'),
            func.coalesce(func.avg(Farm.vegetation_area), 0).label('average_vegetation_area')
        ).where(Farm.farmer_id == farmer_id)
        
        result = await self.session.execute(query)
        averages = result.one()
        return {
            'average_arable_area': averages.average_arable_area,
            'average_vegetation_area': averages.average_vegetation_area
        }
    
    async def find_total_farms_and_hectares_by_farmer_id(self, farmer_id: int):
        query = select(
            func.count(Farm.id).label('total_farms'),
            func.coalesce(func.sum(Farm.total_area), 0).label('total_hectares')  # Substituir NULL por 0
        ).where(Farm.farmer_id == farmer_id)
        
        result = await self.session.execute(query)
        totals = result.one()
        return {
            'farm_count': totals.total_farms,
            'total_hectares': totals.total_hectares
        }

    async def find_farms_by_state_and_farmer_id(self, farmer_id: int, state: str):
        result = await self.session.execute(
                select(Farm)
                .where(Farm.farmer_id == farmer_id, Farm.state == state)
                .options(
                    selectinload(Farm.crops).selectinload(Crop.culture)
                )
        )
        return result.mappings().all()

            
    async def find_farms_ordered_by_vegetation_area_desc_by_farmer_id(self, farmer_id: int):
        query = select(Farm).where(Farm.farmer_id == farmer_id).order_by(Farm.vegetation_area.desc()).options(
                    selectinload(Farm.crops).selectinload(Crop.culture)
                )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def find_farms_ordered_by_arable_area_desc_by_farmer_id(self, farmer_id: int):
        query = select(Farm).where(Farm.farmer_id == farmer_id).order_by(Farm.arable_area.desc()).options(
                    selectinload(Farm.crops).selectinload(Crop.culture)
                )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create_farm_for_a_farmer(self, farmer_id: int, farm: dict):
        stmt = (
            insert(Farm)
            .values(
                name=farm["name"],
                arable_area=farm["arable_area"],
                vegetation_area=farm["vegetation_area"],
                total_area=farm["total_area"],
                farmer_id=farmer_id,
                city=farm["city"],
                state=farm["state"],
            )
            .returning(Farm)
        )

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()

            created_farm = result.scalars().first()
            return created_farm
        except Exception as e:
            await self.session.rollback()
            raise e


    async def update_farm_by_id(self, farm_id: int, farm: dict):
        try:
            stmt = (
                update(Farm)
                .where(Farm.id == farm_id)
                .values(
                    name=farm["name"],
                    arable_area=farm["arable_area"],
                    vegetation_area=farm["vegetation_area"],
                    total_area=farm["total_area"],
                    city=farm["city"],
                    state=farm["state"]
                )
                .returning(Farm)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_farm = result.scalars().first()

            return updated_farm
        except Exception as e:
            await self.session.rollback()
            raise e


    async def delete_farm_by_id(self, farm_id: int):
        try:
            result = await self.session.execute(
                delete(Farm)
                .where(Farm.id == farm_id)
            )
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            raise e