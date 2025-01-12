from fastapi import APIRouter, Body, Query
from adapters.inbound.http.inbound_farm_adapter import InboundFarmAdapter
from adapters.inbound.http.schemas import FarmSchema

class FarmController:
    def __init__(self, inbound_farm_adapter: InboundFarmAdapter):
        self.router = APIRouter()
        self.inbound_farm_adapter = inbound_farm_adapter
        self.router.add_api_route(
            "/api/v1/farmer/{farmer_id}/farm", 
            self.create_farm_for_a_farmer, 
            methods=["POST"], 
            status_code=201
        )

        self.router.add_api_route(
            "/api/v1/farm", 
            self.find_farm, 
            methods=["GET"]
        )
        self.router.add_api_route(
            "/api/v1/farm/{farm_id}", 
            self.update_farm_by_id, 
            methods=["PUT"]
        )
        self.router.add_api_route(
            "/api/v1/farm/{farm_id}", 
            self.delete_farm_by_id, 
            methods=["DELETE"]
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

    async def create_farm_for_a_farmer(self, farmer_id: int, farm: FarmSchema = Body(...)):
        return await self.inbound_farm_adapter.create_farm_for_a_farmer(farmer_id, farm)
    
    async def update_farm_by_id(self, farm_id: int, farm: FarmSchema = Body(...)):
        return await self.inbound_farm_adapter.update_farm_by_id(farm_id, farm)
    
    async def delete_farm_by_id(self, farm_id: int):
        return await self.inbound_farm_adapter.delete_farm_by_id(farm_id)

    def get_router(self):
        return self.router