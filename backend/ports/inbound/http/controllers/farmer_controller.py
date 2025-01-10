from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter
from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.error.bad_request_error import BadRequestError
from domain.farm.invalid_area_error import InvalidAreaError
from fastapi import APIRouter, Body, Query

class FarmerController:
    def __init__(self, farmer_adapter: InboundFarmerAdapter):
        self.router = APIRouter()
        self.farmer_adapter = farmer_adapter
        self.router.add_api_route("/api/v1/farmer", self.create_farmer, methods=["POST"])
        self.router.add_api_route("/api/v1/farmer", self.find_farmers_paginated_and_with_query, methods=["GET"])

    async def create_farmer(self, farm_data: FarmerSchema = Body(...)):
        try:
            await self.farmer_adapter.create_farmer(farm_data)
            return {"message": "Farmer created successfully"}
        except InvalidAreaError as e:
            raise BadRequestError(e.message)
    
    async def find_farmers_paginated_and_with_query(self, limit: int = Query(10), page: int = Query(0), query: str = Query(None)):
        if limit > 100:
            raise BadRequestError("Limit can be at most 100")

        return (await self.farmer_adapter.find_farmers_paginated_and_with_query(limit, page, query))

    def get_router(self):
        return self.router