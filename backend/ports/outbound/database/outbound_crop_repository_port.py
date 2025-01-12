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
            .join(Crop.culture)
            .where(Culture.name == culture_name)
            .where(Farm.farmer_id == farmer_id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def create_crop_for_a_farm_and_return_culture_name(self, farm_id: int, crop: dict):
        new_crop = Crop(
            date=crop["date"],
            farm_id=farm_id,
            culture_id=crop["culture"]["id"],
        )
        self.session.add(new_crop)
        await self.session.commit()
        await self.session.refresh(new_crop)
        
        stmt = (
            select(
                Crop.id,
                Crop.date,
                Culture.name.label("culture_name"),
                Culture.id.label("culture_id"),
                Farm.id.label("farm_id"),
            )
            .join(Culture, Culture.id == Crop.culture_id)
            .join(Farm, Farm.id == Crop.farm_id)
            .where(Crop.id == new_crop.id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().first()
    
    async def update_crop_by_id(self, crop_id: int, crop: dict):
        d = crop.model_dump()
        
        # Atualizar os dados do crop
        stmt_update = (
            update(Crop)
            .where(Crop.id == crop_id)
            .values(
                date=d["date"],
                culture_id=d["culture"]["id"],
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt_update)
        await self.session.commit()
        
        # Consultar os dados atualizados, incluindo culture_name
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

    async def delete_crop_by_id(self, crop_id: int):
        stmt = delete(Crop).where(Crop.id == crop_id)
        await self.session.execute(stmt)
        await self.session.commit()

