from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter
from adapters.inbound.http.schemas import FarmerSchema
from domain.farm.invalid_area_error import InvalidAreaError
from fastapi import APIRouter, HTTPException, Body

class FarmerController:
    def __init__(self, farmer_adapter: InboundFarmerAdapter):
        self.router = APIRouter()
        self.farmer_adapter = farmer_adapter
        self.router.add_api_route("/farmer", self.create_farmer, methods=["POST"])

    async def create_farmer(self, farm_data: FarmerSchema = Body(...)):
        try:
            self.farmer_adapter.create_farmer(farm_data)
            return {"message": "Farmer created successfully"}
        except InvalidAreaError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_router(self):
        return self.router