from adapters.inbound.http.schemas import FarmSchema
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort

class InboundFarmAdapter:
    def __init__(self, outbound_farm_repository_port: OutboundFarmRepositoryPort):
        self.outbound_farm_repository_port = outbound_farm_repository_port

    async def find_farms_by_state_and_farmer_id(self, farmer_id: int, state: str):
        return await self.outbound_farm_repository_port.find_farms_by_state_and_farmer_id(farmer_id, state)
    
    async def find_farms_ordered_by_vegetation_area_desc_by_farmer_id(self, farmer_id: int):
        return await self.outbound_farm_repository_port.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id)

    async def find_farms_ordered_by_arable_area_desc_by_farmer_id(self, farmer_id: int):
        return await self.outbound_farm_repository_port.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id)
    
    async def create_farm_for_a_farmer(self, farmer_id: int, farm: FarmSchema):
        d = farm.dict()
        return await self.outbound_farm_repository_port.create_farm_for_a_farmer(farmer_id, d)
    
    async def update_farm_by_id(self, farm_id: int, farm: dict):
        return await self.outbound_farm_repository_port.update_farm_by_id(farm_id, farm)
    
    async def delete_farm_by_id(self, farm_id: int):
        return await self.outbound_farm_repository_port.delete_farm_by_id(farm_id)