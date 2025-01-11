from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort

class InboundCropAdapter:
    def __init__(self, outbound_crop_repository_port: OutboundCropRepositoryPort):
        self.outbound_crop_repository_port = outbound_crop_repository_port

    async def find_crops_by_culture_id(self, culture_id: int):
        return await self.outbound_crop_repository_port.find_crops_by_culture_id(culture_id)