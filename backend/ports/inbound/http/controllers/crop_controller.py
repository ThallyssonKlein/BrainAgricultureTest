from fastapi import APIRouter

from adapters.inbound.http.inbound_crop_adapter import InboundCropAdapter

class CropController:
    def __init__(self, inbound_crop_adapter: InboundCropAdapter):
        self.router = APIRouter()
        self.inbound_crop_adapter = inbound_crop_adapter
        self.router.add_api_route(
            "/api/v1/crop", 
            self.find_crops_where_associated_culture_has_the_name_and_by_farmer_id, 
            methods=["GET"]
        )


    async def find_crops_where_associated_culture_has_the_name_and_by_farmer_id(self, culture_name: str, farmer_id: int):
        return await self.inbound_crop_adapter.find_crops_where_associated_culture_has_the_name_and_by_farmer_id(culture_name, farmer_id)

    def get_router(self):
        return self.router