from adapters.inbound.http.schemas import CropSchema
from domain.crop_service.crop_service import CropService
from domain.crop_service.culture_not_found_error import CultureNotFoundError
from domain.crop_service.farm_not_found_error import FarmNotFoundError
from ports.inbound.http.error.bad_request_error import BadRequestError
from ports.inbound.http.error.not_found_error import NotFoundError
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort
from shared.loggable import Loggable

class InboundCropAdapter(Loggable):
    def __init__(self, outbound_crop_repository_port: OutboundCropRepositoryPort, crop_service: CropService):
        Loggable.__init__(self, prefix="InboundCropAdapter")
        self.outbound_crop_repository_port = outbound_crop_repository_port
        self.crop_service = crop_service

    async def find_crops(self, culture_name: str, farmer_id: int, trace_id: str):
        if culture_name and farmer_id:
            self.log.info(f"Finding crops with culture_name: {culture_name} and farmer_id: {farmer_id}", trace_id)
            return await self.outbound_crop_repository_port.find_crops_by_culture_name_and_farmer_id(culture_name, farmer_id, trace_id)
        else:
            self.log.error("Invalid query parameters", trace_id)
            raise BadRequestError("Invalid query parameters")
    
    async def create_crop_for_a_farm_and_return_culture(self, farm_id: int, crop: CropSchema, trace_id):
        c = crop.model_dump()
        self.log.info(f"Creating crop for farm with id: {farm_id} and data: {c}", trace_id)
        try:
            return await self.crop_service.create_crop_for_a_farm_and_return_culture(farm_id, c, trace_id)
        except CultureNotFoundError:
            self.log.error("Culture not found", trace_id)
            raise NotFoundError("Culture not found")
        except FarmNotFoundError:
            self.log.error("Farm not found", trace_id)
            raise NotFoundError("Farm not found")

    async def update_crop_by_id(self, crop_id: int, crop: CropSchema, trace_id):
        c = crop.model_dump()
        self.log.info(f"Updating crop with id: {crop_id} and data: {c}", trace_id)
        try:
            return await self.outbound_crop_repository_port.update_crop_by_id(crop_id, c, trace_id)
        except ValueError as e:
            if e.args[0] == "Crop not found":
                self.log.error("Crop not found", trace_id)
                raise NotFoundError("Crop not found")
    
    async def delete_crop_by_id(self, crop_id: int, trace_id: str):
        self.log.info(f"Deleting crop with id: {crop_id}")
        result = await self.outbound_crop_repository_port.delete_crop_by_id(crop_id, trace_id)
        if result.rowcount == 0:
            self.log.error("Crop not found", trace_id)
            raise NotFoundError("Crop not found")