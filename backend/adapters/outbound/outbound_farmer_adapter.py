from ports.outbound.database.outbound_farmer_repository_port import OutboundFarmerRepositoryPort
from shared.loggable import Loggable

class OutboundFarmerAdapter(Loggable):
    def __init__(self, outbound_farmer_repository_port: OutboundFarmerRepositoryPort):
        Loggable.__init__(self, prefix="OutboundFarmerAdapter")
        self.outbound_farmer_repository_port = outbound_farmer_repository_port
    
    async def find_farmer_by_id(self, farmer_id: int, trace_id: str):
        self.log.info(f"Finding farmer with id: {farmer_id}", trace_id)
        return await self.outbound_farmer_repository_port.find_farmer_by_id(farmer_id, trace_id)