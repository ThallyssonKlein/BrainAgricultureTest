from sqlalchemy.ext.asyncio import AsyncSession

from brainagriculturetest.src.ports.outbound.database.models import Crop

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
