from adapters.outbound.outbound_crop_adapter import OutboundCropAdapter
from adapters.outbound.outbound_culture_adapter import OutboundCultureAdapter
from adapters.outbound.outbound_farm_adapter import OutboundFarmAdapter
from domain.crop_service.culture_not_found_error import CultureNotFoundError
from domain.crop_service.farm_not_found_error import FarmNotFoundError
from shared.loggable import Loggable

class CropService(Loggable):
    def __init__(self, outbound_crop_adapter: OutboundCropAdapter, outbound_culture_adapter: OutboundCultureAdapter, outbound_farm_adapter: OutboundFarmAdapter):
        self.outbound_crop_adapter = outbound_crop_adapter
        self.outbound_culture_adapter = outbound_culture_adapter
        self.outbound_farm_adapter = outbound_farm_adapter
        Loggable.__init__(self, prefix="CropService")
    
    async def create_crop_for_a_farm_and_return_culture(self, farm_id: int, c: dict, trace_id: str):
        self.log.info(f"Validating culture with id: {c['culture']['id']}", trace_id)
        culture = await self.outbound_culture_adapter.find_culture_by_id(c['culture']['id'], trace_id)

        if not culture:
            self.log.error(f"Culture with id {c['culture']['id']} not found", trace_id)
            raise CultureNotFoundError()
        
        self.log.info(f"Validating farm with id: {farm_id}", trace_id)
        farm = await self.outbound_farm_adapter.find_farm_by_id(farm_id, trace_id)

        if not farm:
            self.log.error(f"Farm with id {farm_id} not found", trace_id)
            raise FarmNotFoundError()

        self.log.info(f"Creating crop for farm with id: {farm_id} and data: {c}", trace_id)
        return await self.outbound_crop_adapter.create_crop_for_a_farm_and_return_with_culture(farm_id, c, trace_id)