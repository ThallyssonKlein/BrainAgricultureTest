from sqlalchemy import delete, literal, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ports.outbound.database.models import Crop, Culture, Farm

class OutboundCropRepositoryPort:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_crop(self, farm_id: int, crop_data: dict, culture_id: int) -> Crop:
        crop = Crop(
            date=crop_data["date"],
            farm_id=farm_id,
            culture_id=culture_id,
        )
        self.session.add(crop)
        await self.session.commit()
        await self.session.refresh(crop)
        return crop
    
    async def find_crops_by_culture_name_and_farmer_id(self, culture_name: str, farmer_id: int):
        stmt = (
            select(
                Crop.id,
                Crop.farm_id,
                Crop.date,
                Crop.culture_id,
                literal(culture_name).label("culture_name")
            )
            .join(Crop.farm)
            .join(Crop.culture)
            .where(Culture.name == culture_name)
            .where(Farm.farmer_id == farmer_id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def create_crop_for_a_farm_and_return_culture_name(self, farm_id: int, crop: dict):
        try:
            stmt = (
                insert(Crop)
                .values(
                    date=crop["date"],
                    farm_id=farm_id,
                    culture_id=crop["culture"]["id"]
                )
                .returning(
                    Crop.id,
                    Crop.date,
                    Culture.name.label("culture_name"),
                    Culture.id.label("culture_id"),
                    Farm.id.label("farm_id")
                )
            )

            stmt = stmt.join(Culture, Culture.id == Crop.culture_id).join(Farm, Farm.id == Crop.farm_id)

            result = await self.session.execute(stmt)
            await self.session.commit()

            created_crop = result.mappings().first()

            if not created_crop:
                raise ValueError("Failed to create crop or retrieve culture name.")

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
                select(
                    Crop.id,
                    Crop.date,
                    Culture.name.label("culture_name"),
                    Culture.id.label("culture_id"),
                    Farm.id.label("farm_id"),
                )
                .join(Culture, Culture.id == Crop.culture_id)
                .join(Farm, Farm.id == Crop.farm_id)
                .where(Crop.id == crop_id)
            )
            result = await self.session.execute(stmt_select)
            return result.mappings().first()
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

