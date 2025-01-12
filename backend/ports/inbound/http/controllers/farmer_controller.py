from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter
from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.error.bad_request_error import BadRequestError
from fastapi import APIRouter, Body, Query

class FarmerController:
    def __init__(self, farmer_adapter: InboundFarmerAdapter):
        self.router = APIRouter()
        self.farmer_adapter = farmer_adapter
        self.router.add_api_route("/api/v1/farmer", self.create_farmer, methods=["POST"], status_code=201)
        self.router.add_api_route("/api/v1/farmer", self.find_farmers_paginated_and_with_query, methods=["GET"], status_code=200)
        self.router.add_api_route("/api/v1/farmer/{farmer_id}", self.update_farmer_by_id, methods=["PUT"], status_code=200)
        self.router.add_api_route("/api/v1/farmer/{farmer_id}", self.delete_farmer_by_id, methods=["DELETE"], status_code=200)

    async def create_farmer(self, farm_data: FarmerSchema = Body(...)):
        return await self.farmer_adapter.create_farmer(farm_data)
    
    async def update_farmer_by_id(self, farmer_id: int, farm_data: FarmerSchema = Body(...)):
        return await self.farmer_adapter.update_farmer(farmer_id, farm_data)
    
    async def find_farmers_paginated_and_with_query(self, limit: int = Query(10), page: int = Query(0), query: str = Query(None)):
        if limit > 100:
            raise BadRequestError("Limit can be at most 100")

        return await self.farmer_adapter.find_farmers_paginated_and_with_query(limit, page, query)
    
    async def delete_farmer_by_id(self, farmer_id: int):
        return await self.farmer_adapter.delete_farmer_by_id(farmer_id)

    def get_router(self):
        return self.router