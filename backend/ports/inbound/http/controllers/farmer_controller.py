from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter
from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.error.bad_request_error import BadRequestError
from fastapi import APIRouter, Body, Query, Request

from shared.loggable import Loggable

class FarmerController(Loggable):
    def __init__(self, farmer_adapter: InboundFarmerAdapter):
        Loggable.__init__(self, prefix="FarmerController")
        self.router = APIRouter()
        self.farmer_adapter = farmer_adapter
        self.router.add_api_route("/api/v1/farmer", self.create_farmer, methods=["POST"], status_code=201)
        self.router.add_api_route("/api/v1/farmer", self.find_farmers_paginated_and_with_query, methods=["GET"], status_code=200)
        self.router.add_api_route("/api/v1/farmer/{farmer_id}", self.update_farmer_by_id, methods=["PUT"], status_code=200)
        self.router.add_api_route("/api/v1/farmer/{farmer_id}", self.delete_farmer_by_id, methods=["DELETE"], status_code=200)

    async def create_farmer(self, request: Request, farm_data: FarmerSchema = Body(...)):
        self.log.info(f"Request received to create farmer with data: {farm_data}", request.state.trace_id)
        return await self.farmer_adapter.create_farmer(farm_data, request.state.trace_id)
    
    async def update_farmer_by_id(self, request: Request, farmer_id: int, farm_data: FarmerSchema = Body(...)):
        self.log.info(f"Request received to update farmer with data: {farm_data}", request.state.trace_id)
        return await self.farmer_adapter.update_farmer(farmer_id, farm_data, request.state.trace_id)
    
    async def find_farmers_paginated_and_with_query(self, request: Request, limit: int = Query(10), page: int = Query(0), query: str = Query(None)):
        self.log.info(f"Request received to find farmers with limit: {limit}, page: {page}, query: {query}", request.state.trace_id)
        if limit > 100:
            self.log.error("Limit can be at most 100")
            raise BadRequestError("Limit can be at most 100")

        return await self.farmer_adapter.find_farmers_paginated_and_with_query(limit, page, query, request.state.trace_id)
    
    async def delete_farmer_by_id(self, request: Request, farmer_id: int):
        self.log.info(f"Request received to delete farmer with id: {farmer_id}", request.state.trace_id)
        await self.farmer_adapter.delete_farmer_by_id(farmer_id, request.state.trace_id)
        return {"message": "Farmer deleted"}

    def get_router(self):
        return self.router