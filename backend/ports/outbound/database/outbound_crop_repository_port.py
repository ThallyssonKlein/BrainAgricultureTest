from sqlalchemy import literal, select
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
    
    async def find_crops_where_associated_culture_has_the_name_and_by_farmer_id(self, culture_name: str, farmer_id: int):
        stmt = (
            select(
                Crop.id,
                Crop.farm_id,
                Crop.date,
                Crop.culture_id,
                literal(culture_name).label("culture_name")
            )
            .join(Crop.farm)
            .where(Culture.name == culture_name)
            .where(Farm.farmer_id == farmer_id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()
