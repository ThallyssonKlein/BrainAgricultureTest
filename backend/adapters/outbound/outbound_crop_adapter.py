from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort
from shared.loggable import Loggable

class OutboundCropAdapter(Loggable):
    def __init__(self, outbound_crop_repository_port: OutboundCropRepositoryPort):
        Loggable.__init__(self, prefix="OutboundCropAdapter")
        self.outbound_crop_repository_port = outbound_crop_repository_port
    
    async def create_crop_for_a_farm_and_return_with_culture(self, farm_id: int, crop: dict, trace_id: str):
        self.log.info(f"Creating crop for farm with id: {farm_id} and data: {crop}", trace_id)
        return await self.outbound_crop_repository_port.create_crop_for_a_farm_and_return_with_culture(farm_id, crop, trace_id)