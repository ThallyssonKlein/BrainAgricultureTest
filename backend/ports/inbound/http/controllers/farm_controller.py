from fastapi import APIRouter, Query
from adapters.inbound.http.inbound_farm_adapter import InboundFarmAdapter

class FarmController:
    def __init__(self, inbound_farm_adapter: InboundFarmAdapter):
        self.router = APIRouter()
        self.inbound_farm_adapter = inbound_farm_adapter
        self.router.add_api_route(
            "/api/v1/farm", 
            self.find_farm, 
            methods=["GET"]
        )

    async def find_farm(self, farmer_id: int, state: str = Query(None), order_by: str = Query(None)):
        if state:
            return await self.find_farm_by_farmer_id_and_state(farmer_id, state)
        elif order_by == "vegetation_area_desc":
            return await self.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id)
        elif order_by == "arable_area_desc":
            return await self.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id)
        else:
            return {"error": "Invalid parameters"}

    async def find_farm_by_farmer_id_and_state(self, farmer_id: int, state: str):
        return await self.inbound_farm_adapter.find_farms_by_state_and_farmer_id(farmer_id, state)
    
    async def find_farms_ordered_by_vegetation_area_desc_by_farmer_id(self, farmer_id: int):
        return await self.inbound_farm_adapter.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id)

    async def find_farms_ordered_by_arable_area_desc_by_farmer_id(self, farmer_id: int):
        return await self.inbound_farm_adapter.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id)

    def get_router(self):
        return self.router