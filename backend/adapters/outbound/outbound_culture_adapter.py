from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort
from shared.loggable import Loggable

class OutboundCultureAdapter(Loggable):
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort):
        Loggable.__init__(self, prefix="OutboundCultureAdapter")
        self.outbound_culture_repository_port = outbound_culture_repository_port
    
    async def find_culture_by_id(self, culture_id: int, trace_id: str):
        self.log.info(f"Finding culture with id: {culture_id}", trace_id)
        return await self.outbound_culture_repository_port.find_culture_by_id(culture_id, trace_id)
    
    async def get_by_farmer_id_and_name(self, farmer_id: int, culture_name: str, trace_id: str):
        self.log.info(f"Getting culture by farmer_id: {farmer_id} and culture_name: {culture_name}", trace_id)
        return await self.outbound_culture_repository_port.get_by_farmer_id_and_name(farmer_id, culture_name, trace_id)
    
    async def create_culture_for_a_farmer(self, farmer_id: int, culture: dict, trace_id: str):
        self.log.info(f"Creating culture for farmer with id: {farmer_id} and data: {culture}", trace_id)
        return await self.outbound_culture_repository_port.create_culture_for_a_farmer(farmer_id, culture, trace_id)
    
    async def update_culture_by_id(self, culture_id: int, culture: dict, trace_id: str):
        self.log.info(f"Updating culture with id: {culture_id} and data: {culture}", trace_id)
        return await self.outbound_culture_repository_port.update_culture_by_id(culture_id, culture, trace_id)