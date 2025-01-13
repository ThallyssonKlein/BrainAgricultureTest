from adapters.outbound.outbound_farm_adapter import OutboundFarmAdapter
from adapters.outbound.outbound_farmer_adapter import OutboundFarmerAdapter
from domain.farm.farmer_not_found_error import FarmerNotFoundError
from shared.loggable import Loggable

class FarmService(Loggable):
    def __init__(self, outbound_farm_adapter: OutboundFarmAdapter, outbound_farmer_adapter: OutboundFarmerAdapter):
        Loggable.__init__(self, prefix="FarmService")
        self.outbound_farm_adapter = outbound_farm_adapter
        self.outbound_farmer_adapter = outbound_farmer_adapter
    
    async def create_farm_for_a_farmer(self, farmer_id: int, farm: dict, trace_id: str):
        self.log.info(f"Finding farmer with id: {farmer_id}", trace_id)
        farmer = await self.outbound_farmer_adapter.find_farmer_by_id(farmer_id, trace_id)

        if not farmer:
            self.log.error(f"Farmer with id: {farmer_id} not found", trace_id)
            raise FarmerNotFoundError()
        

        self.log.info(f"Creating farm for farmer with id: {farmer_id} and data: {farm}", trace_id)
        return await self.outbound_farm_adapter.create_farm_for_a_farmer(farmer_id, farm, trace_id)
    
