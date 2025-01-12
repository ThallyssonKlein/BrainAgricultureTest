from fastapi import APIRouter, Path
from adapters.inbound.http.inbound_dashboard_adapter import InboundDashboardAdapter

class DashboardController:
    def __init__(self, dashboard_adapter: InboundDashboardAdapter):
        self.router = APIRouter()
        self.dashboard_adapter = dashboard_adapter
        self.router.add_api_route(
            "/api/v1/dashboard/{farmer_id}", 
            self.get_dashboard_data, 
            methods=["GET"]
        )

    async def get_dashboard_data(self, farmer_id: int = Path(..., description="The ID of the farmer")):
        return await self.dashboard_adapter.get_dashboard_data(farmer_id)

    def get_router(self):
        return self.router