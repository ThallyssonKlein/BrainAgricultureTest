from fastapi import APIRouter, Body, Path, Request

from adapters.inbound.http.inbound_crop_adapter import InboundCropAdapter
from adapters.inbound.http.schemas import CropSchema
from shared.loggable import Loggable

class CropController(Loggable):
    def __init__(self, inbound_crop_adapter: InboundCropAdapter):
        Loggable.__init__(self, prefix="CropController")
        self.router = APIRouter()
        self.inbound_crop_adapter = inbound_crop_adapter
        self.router.add_api_route(
            "/api/v1/farm/{farm_id}/crop",
            self.create_crop_for_a_farm_and_return_culture,
            methods=["POST"],
            status_code=201
        )
        self.router.add_api_route(
            "/api/v1/crop", 
            self.find_crops, 
            methods=["GET"],
            status_code=200
        )
        self.router.add_api_route(
            "/api/v1/crop/{crop_id}",
            self.update_crop_by_id,
            methods=["PUT"],
            status_code=200
        )
        self.router.add_api_route(
            "/api/v1/crop/{crop_id}",
            self.delete_crop_by_id,
            methods=["DELETE"],
            status_code=200
        )


    async def find_crops(self, request: Request, culture_name: str, farmer_id: int):
        self.log.info(f"Request received to find crops with culture_name: {culture_name} and farmer_id: {farmer_id}", request.state.trace_id)
        return await self.inbound_crop_adapter.find_crops(culture_name, farmer_id, request.state.trace_id)
    
    async def create_crop_for_a_farm_and_return_culture(self, request: Request, farm_id: int = Path(...), crop: CropSchema = Body(...)):
        self.log.info(f"Request received to create crop for farm with id: {farm_id} and data: {crop}", request.state.trace_id)
        return await self.inbound_crop_adapter.create_crop_for_a_farm_and_return_culture(farm_id, crop, request.state.trace_id)

    async def update_crop_by_id(self, request: Request, crop_id: int = Path(...), crop: CropSchema = Body(...)):
        self.log.info(f"Request received to update crop with id: {crop_id} and data: {crop}", request.state.trace_id)
        return await self.inbound_crop_adapter.update_crop_by_id(crop_id, crop, request.state.trace_id)
    
    async def delete_crop_by_id(self, request: Request, crop_id: int = Path(...)):
        self.log.info(f"Request received to delete crop with id: {crop_id}", request.state.trace_id)
        await self.inbound_crop_adapter.delete_crop_by_id(crop_id, request.state.trace_id)
    
    def get_router(self):
        return self.router