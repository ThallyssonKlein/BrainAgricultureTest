from fastapi import APIRouter, Body, Path

from adapters.inbound.http.inbound_crop_adapter import InboundCropAdapter
from adapters.inbound.http.schemas import CropSchema

class CropController:
    def __init__(self, inbound_crop_adapter: InboundCropAdapter):
        self.router = APIRouter()
        self.inbound_crop_adapter = inbound_crop_adapter
        self.router.add_api_route(
            "/api/v1/crop", 
            self.find_crops_where_associated_culture_has_the_name_and_by_farmer_id, 
            methods=["GET"]
        )
        self.router.add_api_route(
            "/api/v1/farm/{farm_id}/crop",
            self.create_crop_for_a_farm,
            methods=["POST"],
            status_code=201
        )


    async def find_crops_where_associated_culture_has_the_name_and_by_farmer_id(self, culture_name: str, farmer_id: int):
        return await self.inbound_crop_adapter.find_crops_where_associated_culture_has_the_name_and_by_farmer_id(culture_name, farmer_id)
    
    async def create_crop_for_a_farm(self, farm_id: int = Path(...), crop: CropSchema = Body(...)):
        return await self.inbound_crop_adapter.create_crop_for_a_farm(farm_id, crop)

    def get_router(self):
        return self.router