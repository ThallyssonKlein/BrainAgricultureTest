from fastapi import APIRouter, Body, Query, Request
from adapters.inbound.http.inbound_farm_adapter import InboundFarmAdapter
from adapters.inbound.http.schemas import FarmSchema
from shared.loggable import Loggable

class FarmController(Loggable):
    def __init__(self, inbound_farm_adapter: InboundFarmAdapter):
        Loggable.__init__(self, prefix="FarmController")
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
            self.find_farms, 
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

    async def find_farms(self, request: Request, farmer_id: int, state: str = Query(None), order_by: str = Query(None)):
        self.log.info(f"Request received to find farms with farmer_id: {farmer_id}, state: {state}, order_by: {order_by}", request.state.trace_id)
        if state:
            return await self.find_farm_by_farmer_id_and_state(farmer_id, state, request.state.trace_id)
        elif order_by == "vegetation_area_desc":
            return await self.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id, request.state.trace_id)
        elif order_by == "arable_area_desc":
            return await self.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id, request.state.trace_id)
        else:
            self.log.error("Invalid parameters", request.state.trace_id)
            return {"error": "Invalid parameters"}

    async def find_farm_by_farmer_id_and_state(self, request: Request, farmer_id: int, state: str):
        self.log.info(f"Request received to find farms with farmer_id: {farmer_id} and state: {state}", request.state.trace_id)
        return await self.inbound_farm_adapter.find_farms_by_state_and_farmer_id(farmer_id, state, request.state.trace_id)
    
    async def find_farms_ordered_by_vegetation_area_desc_by_farmer_id(self, request: Request, farmer_id: int):
        self.log.info(f"Request received to find farms ordered by vegetation area descending with farmer_id: {farmer_id}", request.state.trace_id)
        return await self.inbound_farm_adapter.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id, request.state.trace_id)

    async def find_farms_ordered_by_arable_area_desc_by_farmer_id(self, request: Request, farmer_id: int):
        self.log.info(f"Request received to find farms ordered by arable area descending with farmer_id: {farmer_id}", request.state.trace_id)
        return await self.inbound_farm_adapter.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id, request.state.trace_id)

    async def create_farm_for_a_farmer(self, request: Request, farmer_id: int, farm: FarmSchema = Body(...)):
        self.log.info(f"Request received to create farm for farmer with id: {farmer_id} and data: {farm}", request.state.trace_id)
        return await self.inbound_farm_adapter.create_farm_for_a_farmer(farmer_id, farm, request.state.trace_id)
    
    async def update_farm_by_id(self, request: Request, farm_id: int, farm: FarmSchema = Body(...)):
        self.log.info(f"Request received to update farm with id: {farm_id} and data: {farm}", request.state.trace_id)
        return await self.inbound_farm_adapter.update_farm_by_id(farm_id, farm, request.state.trace_id)
    
    async def delete_farm_by_id(self, request: Request, farm_id: int):
        self.log.info(f"Request received to delete farm with id: {farm_id}", request.state.trace_id)
        await self.inbound_farm_adapter.delete_farm_by_id(farm_id, request.state.trace_id)
        return {"message": "Farm deleted"}

    def get_router(self):
        return self.router