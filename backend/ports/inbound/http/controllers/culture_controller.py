from fastapi import APIRouter, Body, Path, Request

from adapters.inbound.http.inbound_culture_adapter import InboundCultureAdapter
from adapters.inbound.http.schemas import CultureSchema
from shared.loggable import Loggable

class CultureController(Loggable):
    def __init__(self, inbound_culture_adapter: InboundCultureAdapter):
        Loggable.__init__(self, prefix="CultureController")
        self.router = APIRouter()
        self.inbound_culture_adapter = inbound_culture_adapter
        self.router.add_api_route(
            "/api/v1/farmer/{farmer_id}/culture", 
            self.create_a_culture_for_a_farmer, 
            methods=["POST"],
            status_code=201
        )
        self.router.add_api_route(
            "/api/v1/farmer/{farmer_id}/culture", 
            self.get_cultures_for_a_farmer, 
            methods=["GET"],
            status_code=200
        )

        self.router.add_api_route(
            "/api/v1/culture/{culture_id}", 
            self.update_culture_by_id, 
            methods=["PUT"],
            status_code=200
        )
        self.router.add_api_route(
            "/api/v1/culture/{culture_id}", 
            self.delete_culture_by_id, 
            methods=["DELETE"],
            status_code=200
        )

    async def create_a_culture_for_a_farmer(self, request: Request, farmer_id: int = Path(...), culture: CultureSchema = Body(...)):
        self.log.info(f"Request received to create culture for farmer with id: {farmer_id} and data: {culture}", request.state.trace_id)
        return await self.inbound_culture_adapter.create_culture_for_a_farmer(farmer_id, culture, request.state.trace_id)
    
    async def get_cultures_for_a_farmer(self, request: Request, farmer_id: int = Path(...)):
        self.log.info(f"Request received to get cultures for farmer with id: {farmer_id}", request.state.trace_id)
        return await self.inbound_culture_adapter.get_cultures_for_a_farmer(farmer_id, request.state.trace_id)
    
    async def update_culture_by_id(self, request: Request, culture_id: int = Path(...), culture: CultureSchema = Body(...)):
        self.log.info(f"Request received to update culture with id: {culture_id} and data: {culture}", request.state.trace_id)
        return await self.inbound_culture_adapter.update_culture_by_id(culture_id, culture, request.state.trace_id)
    
    async def delete_culture_by_id(self, request: Request, culture_id: int = Path(...)):
        self.log.info(f"Request received to delete culture with id: {culture_id}", request.state.trace_id)
        await self.inbound_culture_adapter.delete_culture_by_id(culture_id, request.state.trace_id)
        return {"message": "Culture deleted successfully"}
    
    def get_router(self):
        return self.router