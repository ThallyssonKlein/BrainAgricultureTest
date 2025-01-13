from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from shared.loggable import Loggable

class OutboundFarmAdapter(Loggable):
    def __init__(self, outbound_farm_repository_port: OutboundFarmRepositoryPort):
        Loggable.__init__(self, prefix="OutboundFarmAdapter")
        self.outbound_farm_repository_port = outbound_farm_repository_port
    
    async def find_farm_by_id(self, farm_id: int, trace_id: str):
        self.log.info(f"Finding farm with id: {farm_id}", trace_id)
        return await self.outbound_farm_repository_port.find_farm_by_id(farm_id, trace_id)

    async def create_farm_for_a_farmer(self, farmer_id: int, farm: dict, trace_id: str):
        self.log.info(f"Creating farm for farmer with id: {farmer_id} and data: {farm}", trace_id)
        return await self.outbound_farm_repository_port.create_farm_for_a_farmer(farmer_id, farm, trace_id)