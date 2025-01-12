from adapters.inbound.http.schemas import CropSchema
from ports.inbound.http.error.bad_request_error import BadRequestError
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort

class InboundCropAdapter:
    def __init__(self, outbound_crop_repository_port: OutboundCropRepositoryPort):
        self.outbound_crop_repository_port = outbound_crop_repository_port

    async def find_crops(self, culture_name: str, farmer_id: int):
        if culture_name and farmer_id:
            return await self.outbound_crop_repository_port.find_crops_by_culture_name_and_farmer_id(culture_name, farmer_id)
        else:
            raise BadRequestError("Invalid query parameters")
    
    async def create_crop_for_a_farm_and_return_culture_name(self, farm_id: int, crop: CropSchema):
        c = crop.model_dump()
        return await self.outbound_crop_repository_port.create_crop_for_a_farm_and_return_culture_name(farm_id, c)

    async def update_crop_by_id(self, crop_id: int, crop: dict):
        return await self.outbound_crop_repository_port.update_crop_by_id(crop_id, crop)
    
    async def delete_crop_by_id(self, crop_id: int):
        await self.outbound_crop_repository_port.delete_crop_by_id(crop_id)