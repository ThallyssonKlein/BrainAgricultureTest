from fastapi import APIRouter
from adapters.inbound.http.inbound_farm_adapter import InboundFarmAdapter

class FarmController:
    def __init__(self, inbound_farm_adapter: InboundFarmAdapter):
        self.router = APIRouter()
        self.inbound_farm_adapter = inbound_farm_adapter
        self.router.add_api_route(
            "/api/v1/farm", 
            self.find_farm_by_farmer_id_and_state, 
            methods=["GET"]
        )

    async def find_farm_by_farmer_id_and_state(self, farmer_id: int, state: str):
        return await self.inbound_farm_adapter.find_farms_by_state_and_farmer_id(farmer_id, state)

    def get_router(self):
        return self.router