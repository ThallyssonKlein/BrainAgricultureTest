from fastapi import APIRouter, Path, Request
from adapters.inbound.http.inbound_dashboard_adapter import InboundDashboardAdapter
from shared.loggable import Loggable

class DashboardController(Loggable):
    def __init__(self, dashboard_adapter: InboundDashboardAdapter):
        Loggable.__init__(self, prefix="DashboardController")
        self.router = APIRouter()
        self.dashboard_adapter = dashboard_adapter
        self.router.add_api_route(
            "/api/v1/dashboard/{farmer_id}", 
            self.get_dashboard_data, 
            methods=["GET"]
        )

    async def get_dashboard_data(self, request: Request, farmer_id: int = Path(..., description="The ID of the farmer")):
        self.log.info(f"Request received to get dashboard data for farmer with id: {farmer_id}", request.state.trace_id)
        return await self.dashboard_adapter.get_dashboard_data(farmer_id, request.state.trace_id)

    def get_router(self):
        return self.router