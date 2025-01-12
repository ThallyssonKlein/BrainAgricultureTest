from fastapi import APIRouter, Body, Path

from adapters.inbound.http.inbound_crop_adapter import InboundCropAdapter
from adapters.inbound.http.schemas import CropSchema

class CropController:
    def __init__(self, inbound_crop_adapter: InboundCropAdapter):
        self.router = APIRouter()
        self.inbound_crop_adapter = inbound_crop_adapter
        self.router.add_api_route(
            "/api/v1/farm/{farm_id}/crop",
            self.create_crop_for_a_farm_and_return_culture_name,
            methods=["POST"],
            status_code=201
        )
        self.router.add_api_route(
            "/api/v1/crop", 
            self.find_crops_where_associated_culture_has_the_name_and_by_farmer_id, 
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


    async def find_crops_where_associated_culture_has_the_name_and_by_farmer_id(self, culture_name: str, farmer_id: int):
        return await self.inbound_crop_adapter.find_crops_where_associated_culture_has_the_name_and_by_farmer_id(culture_name, farmer_id)
    
    async def create_crop_for_a_farm_and_return_culture_name(self, farm_id: int = Path(...), crop: CropSchema = Body(...)):
        return await self.inbound_crop_adapter.create_crop_for_a_farm_and_return_culture_name(farm_id, crop)

    async def update_crop_by_id(self, crop_id: int = Path(...), crop: CropSchema = Body(...)):
        return await self.inbound_crop_adapter.update_crop_by_id(crop_id, crop)
    
    async def delete_crop_by_id(self, crop_id: int = Path(...)):
        await self.inbound_crop_adapter.delete_crop_by_id(crop_id)
    
    def get_router(self):
        return self.router