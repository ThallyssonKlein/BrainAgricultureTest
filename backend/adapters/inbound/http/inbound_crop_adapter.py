from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort

class InboundCropAdapter:
    def __init__(self, outbound_crop_repository_port: OutboundCropRepositoryPort):
        self.outbound_crop_repository_port = outbound_crop_repository_port

    async def find_crops_where_associated_culture_has_the_name_and_by_farmer_id(self, culture_name: str, farmer_id: int):
        return await self.outbound_crop_repository_port.find_crops_where_associated_culture_has_the_name_and_by_farmer_id(culture_name, farmer_id)