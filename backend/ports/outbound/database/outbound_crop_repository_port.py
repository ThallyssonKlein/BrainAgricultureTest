from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ports.outbound.database.models import Crop, Culture, Farm

class OutboundCropRepositoryPort:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_crop(self, farm_id: int, crop_data: dict, culture_id: int) -> Crop:
        try:
            crop = Crop(
                date=crop_data["date"],
                farm_id=farm_id,
                culture_id=culture_id,
            )
            self.session.add(crop)
            await self.session.commit()
            await self.session.refresh(crop)
            return crop
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def find_crops_by_culture_name_and_farmer_id(self, culture_name: str, farmer_id: int):
        try:
            stmt = (
                select(Crop)
                .join(Crop.farm)
                .join(Crop.culture)
                .where(Culture.name == culture_name)
                .where(Farm.farmer_id == farmer_id)
                .options(
                    selectinload(Crop.culture)
                )
            )
            result = await self.session.execute(stmt)
            crops = result.scalars().all()
            return crops
        except Exception as e:
            await self.session.rollback()
            raise e


    async def create_crop_for_a_farm_and_return_with_culture(self, farm_id: int, crop: dict):
        try:
            stmt = (
                insert(Crop)
                .values(
                    date=crop["date"],
                    farm_id=farm_id,
                    culture_id=crop["culture"]["id"]
                )
                .returning(Crop.id)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            crop_id = result.scalar()
            if not crop_id:
                raise ValueError("Failed to create crop.")

            stmt = (
                select(Crop)
                .where(Crop.id == crop_id)
                .options(
                    selectinload(Crop.culture)
                )
            )

            result = await self.session.execute(stmt)
            created_crop = result.scalars().first()

            if not created_crop:
                raise ValueError("Failed to retrieve crop with culture relationship.")

            return created_crop
        except Exception as e:
            await self.session.rollback()
            raise e
    
    async def update_crop_by_id(self, crop_id: int, crop: dict):        
        try:
            stmt_update = (
                update(Crop)
                .where(Crop.id == crop_id)
                .values(
                    date=crop["date"],
                    culture_id=crop["culture"]["id"],
                )
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(stmt_update)
            await self.session.commit()

            stmt_select = (
                select(Crop)
                .where(Crop.id == crop_id)
                .options(
                    selectinload(Crop.culture),
                    selectinload(Crop.farm),
                )
            )

            result = await self.session.execute(stmt_select)
            updated_crop = result.scalars().first()

            if not updated_crop:
                raise ValueError("Crop not found.")

            return updated_crop
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_crop_by_id(self, crop_id: int):
        try:
            stmt = delete(Crop).where(Crop.id == crop_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            raise e

