from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, delete, insert, update
from sqlalchemy.orm import selectinload

from ports.outbound.database.models import Crop, Culture, Farm
from shared.loggable import Loggable

class OutboundFarmRepositoryPort(Loggable):
    def __init__(self, session: AsyncSession):
        Loggable.__init__(self, prefix="OutboundFarmRepositoryPort")
        self.session = session
    
    async def find_farm_counts_grouped_by_state_by_farmer_id(self, farmer_id: int, trace_id: str):
        try:
            query = select(
            Farm.state.label("state"),
            func.count(Farm.id).label('farm_count')
            ).where(Farm.farmer_id == farmer_id).group_by(Farm.state)
            result = await self.session.execute(query)
            return result.mappings().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e
    
    async def find_farms_count_grouped_by_culture_by_farmer_id(self, farmer_id: int, trace_id: str):
        try:
            query = select(
            Culture.name.label('culture'),
            func.count(Farm.id).label('farm_count')
            ).join(Crop, Crop.farm_id == Farm.id).join(Culture, Culture.id == Crop.culture_id).where(Farm.farmer_id == farmer_id).group_by(Culture.name)
            
            result = await self.session.execute(query)
            return result.mappings().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e
    
    async def find_average_land_use_by_farmer_id(self, farmer_id: int, trace_id: str):
        try:
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
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e
    
    async def find_total_farms_and_hectares_by_farmer_id(self, farmer_id: int, trace_id: str):
        try:
            query = select(
            func.count(Farm.id).label('farm_count'),
            func.coalesce(func.sum(Farm.total_area), 0).label('total_hectares')  # Substituir NULL por 0
            ).where(Farm.farmer_id == farmer_id)
            
            result = await self.session.execute(query)
            totals = result.one()
            return {
                'farm_count': totals.farm_count,
                'total_hectares': totals.total_hectares
            }
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e

    async def find_farms_by_state_and_farmer_id(self, farmer_id: int, state: str, trace_id: str):
        try:
            result = await self.session.execute(
            select(Farm)
            .where(Farm.farmer_id == farmer_id, Farm.state == state)
            .options(
                selectinload(Farm.crops).selectinload(Crop.culture)
            )
            )
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e

            
    async def find_farms_ordered_by_vegetation_area_desc_by_farmer_id(self, farmer_id: int, trace_id: str):
        try:
            query = select(Farm).where(Farm.farmer_id == farmer_id).order_by(Farm.vegetation_area.desc()).options(
                    selectinload(Farm.crops).selectinload(Crop.culture)
                )
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e
    
    async def find_farms_ordered_by_arable_area_desc_by_farmer_id(self, farmer_id: int, trace_id: str):
        try:
            query = select(Farm).where(Farm.farmer_id == farmer_id).order_by(Farm.arable_area.desc()).options(
                    selectinload(Farm.crops).selectinload(Crop.culture)
                )
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farms: {e}", trace_id)
            raise e
    
    async def create_farm_for_a_farmer(self, farmer_id: int, farm: dict, trace_id: str):
        try:
            stmt = (
                insert(Farm)
                .values(
                    name=farm["name"],
                    arable_area=farm["arable_area"],
                    vegetation_area=farm["vegetation_area"],
                    total_area=farm["vegetation_area"] + farm["arable_area"],
                    farmer_id=farmer_id,
                    city=farm["city"],
                    state=farm["state"],
                )
                .returning(Farm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            created_farm = result.scalars().first()

            if created_farm:
                await self.session.refresh(
                    created_farm,
                    attribute_names=["crops"]
                )
                for crop in created_farm.crops:
                    await self.session.refresh(crop, attribute_names=["culture"])

            return created_farm
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error creating farm: {e}", trace_id)
            raise e


    async def update_farm_by_id(self, farm_id: int, farm: dict, trace_id: str):
        try:
            stmt = (
                update(Farm)
                .where(Farm.id == farm_id)
                .values(
                    name=farm["name"],
                    arable_area=farm["arable_area"],
                    vegetation_area=farm["vegetation_area"],
                    total_area=farm["vegetation_area"] + farm["arable_area"],
                    city=farm["city"],
                    state=farm["state"]
                )
                .returning(Farm)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_farm = result.scalars().first()

            if updated_farm:
                await self.session.refresh(
                    updated_farm,
                    attribute_names=["crops"]
                )
                for crop in updated_farm.crops:
                    await self.session.refresh(
                        crop,
                        attribute_names=["culture"]
                    )
            else:
                raise ValueError("Farm not found")

            return updated_farm
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error updating farm: {e}", trace_id)
            raise e


    async def delete_farm_by_id(self, farm_id: int, trace_id: str):
        try:
            result = await self.session.execute(
                delete(Farm)
                .where(Farm.id == farm_id)
            )
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error deleting farm: {e}", trace_id)
            raise e
    
    async def find_farm_by_id(self, farm_id: int, trace_id: str):
        try:
            result = await self.session.execute(
                select(Farm)
                .where(Farm.id == farm_id)
            )
            return result.scalars().first()
        except Exception as e:
            await self.session.rollback()
            self.log.error(f"Error finding farm: {e}", trace_id)
            raise e