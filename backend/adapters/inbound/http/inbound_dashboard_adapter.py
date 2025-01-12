from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from shared.loggable import Loggable

class InboundDashboardAdapter(Loggable):
    def __init__(self, outbound_farm_repository: OutboundFarmRepositoryPort):
        Loggable.__init__(self, prefix="InboundDashboardAdapter")
        self.outbound_farm_repository = outbound_farm_repository

    async def get_dashboard_data(self, farmer_id: int, trace_id: str):
        data_for_chats = {
            "farm_count": 0,
            "total_hectares": 0,
            "farm_counts_grouped_by_state": [],
            "farms_count_grouped_by_culture": [],
            "average_land_use": {
                "average_arable_area": 0,
                "average_vegetation_area": 0
            }
        }

        self.log.info(f"Getting dashboard data for farmer with id: {farmer_id}", trace_id)
        result1 = await self.outbound_farm_repository.find_total_farms_and_hectares_by_farmer_id(farmer_id, trace_id)
        data_for_chats["farm_count"] = result1["farm_count"]
        data_for_chats["total_hectares"] = result1["total_hectares"]

        self.log.info(f"Getting farms count grouped by state for farmer with id: {farmer_id}", trace_id)
        result2 = await self.outbound_farm_repository.find_farm_counts_grouped_by_state_by_farmer_id(farmer_id, trace_id)
        data_for_chats["farm_counts_grouped_by_state"] = result2

        self.log.info(f"Getting farms count grouped by culture for farmer with id: {farmer_id}", trace_id)
        result4 = await self.outbound_farm_repository.find_farms_count_grouped_by_culture_by_farmer_id(farmer_id, trace_id)
        data_for_chats["farms_count_grouped_by_culture"] = result4

        self.log.info(f"Getting average land use for farmer with id: {farmer_id}", trace_id)
        result6 = await self.outbound_farm_repository.find_average_land_use_by_farmer_id(farmer_id, trace_id)
        data_for_chats["average_land_use"]["average_arable_area"] = result6["average_arable_area"]
        data_for_chats["average_land_use"]["average_vegetation_area"] = result6["average_vegetation_area"]

        return data_for_chats