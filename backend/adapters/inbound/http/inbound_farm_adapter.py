from adapters.inbound.http.schemas import FarmSchema
from domain.farm.farm_service import FarmService
from domain.farm.farmer_not_found_error import FarmerNotFoundError
from ports.inbound.http.error.not_found_error import NotFoundError
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from shared.loggable import Loggable

class InboundFarmAdapter(Loggable):
    def __init__(self, outbound_farm_repository_port: OutboundFarmRepositoryPort, farm_service: FarmService):
        Loggable.__init__(self, prefix="InboundFarmAdapter")
        self.outbound_farm_repository_port = outbound_farm_repository_port
        self.farm_service = farm_service

    async def find_farms_by_state_and_farmer_id(self, farmer_id: int, state: str, trace_id: str):
        self.log.info(f"Finding farms with farmer_id: {farmer_id} and state: {state}", trace_id)
        return await self.outbound_farm_repository_port.find_farms_by_state_and_farmer_id(farmer_id, state, trace_id)
    
    async def find_farms_ordered_by_vegetation_area_desc_by_farmer_id(self, farmer_id: int, trace_id: str):
        self.log.info(f"Finding farms ordered by vegetation area descending with farmer_id: {farmer_id}", trace_id)
        return await self.outbound_farm_repository_port.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id, trace_id)

    async def find_farms_ordered_by_arable_area_desc_by_farmer_id(self, farmer_id: int, trace_id: str):
        self.log.info(f"Finding farms ordered by arable area descending with farmer_id: {farmer_id}", trace_id)
        return await self.outbound_farm_repository_port.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id, trace_id)
    
    async def create_farm_for_a_farmer(self, farmer_id: int, farm: FarmSchema, trace_id: str):
        self.log.info(f"Creating farm for farmer with id: {farmer_id} and data: {farm}", trace_id)
        d = farm.model_dump()
        try:
            return await self.farm_service.create_farm_for_a_farmer(farmer_id, d, trace_id)
        except FarmerNotFoundError as e:
            self.log.error(f"Farmer with id: {farmer_id} not found", trace_id)
            raise NotFoundError("Farmer not found")
    
    async def update_farm_by_id(self, farm_id: int, farm: FarmSchema, trace_id: str):
        self.log.info(f"Updating farm with id: {farm_id} and data: {farm}", trace_id)
        f = farm.model_dump()
        return await self.outbound_farm_repository_port.update_farm_by_id(farm_id, f, trace_id)
    
    async def delete_farm_by_id(self, farm_id: int, trace_id: str):
        self.log.info(f"Deleting farm with id: {farm_id}", trace_id)
        result = await self.outbound_farm_repository_port.delete_farm_by_id(farm_id, trace_id)
        if result.rowcount == 0:
            self.log.error("Farm not found", trace_id)
            raise NotFoundError("Farm not found")