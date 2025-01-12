from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort

class InboundCropAdapter:
    def __init__(self, outbound_crop_repository_port: OutboundCropRepositoryPort):
        self.outbound_crop_repository_port = outbound_crop_repository_port

    async def find_crops_where_associated_culture_has_the_name_and_by_farmer_id(self, culture_name: str, farmer_id: int):
        return await self.outbound_crop_repository_port.find_crops_where_associated_culture_has_the_name_and_by_farmer_id(culture_name, farmer_id)
    
    async def create_crop_for_a_farm(self, farm_id: int, crop: dict):
        return await self.outbound_crop_repository_port.create_crop_for_a_farm(farm_id, crop)

    async def update_crop_by_id(self, crop_id: int, crop: dict):
        return await self.outbound_crop_repository_port.update_crop_by_id(crop_id, crop)