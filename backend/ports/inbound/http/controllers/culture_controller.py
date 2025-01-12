from fastapi import APIRouter, Body, Path

from adapters.inbound.http.inbound_culture_adapter import InboundCultureAdapter
from adapters.inbound.http.schemas import CultureSchema

class CultureController:
    def __init__(self, inbound_culture_adapter: InboundCultureAdapter):
        self.router = APIRouter()
        self.inbound_culture_adapter = inbound_culture_adapter
        self.router.add_api_route(
            "/api/v1/farmer/{farmer_id}/culture", 
            self.create_a_culture_for_a_farmer, 
            methods=["POST"]
        )

    async def create_a_culture_for_a_farmer(self, farmer_id: int = Path(...), culture: CultureSchema = Body(...)):
        return await self.inbound_culture_adapter.create_culture_for_a_farmer_id(farmer_id, culture)

    def get_router(self):
        return self.router