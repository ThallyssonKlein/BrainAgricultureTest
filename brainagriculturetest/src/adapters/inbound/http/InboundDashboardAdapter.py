from brainagriculturetest.src.ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort


class InboundDashboardAdapter:
    def __init__(self, outbound_farm_repository: OutboundFarmRepositoryPort):
        self.outbound_farm_repository = outbound_farm_repository

    async def get_data_for_chats(self, farmer_id: int):
        data_for_chats = {
            "farm_count": 0,
            "total_hectares": 0,
            "farm_counts_grouped_by_state": [],
            "farms_grouped_by_state": [],
            "farms_count_grouped_by_culture": [],
            "farms_grouped_by_culture": [],
            "average_land_use": {
                "average_arable_area": 0,
                "average_vegetation_area": 0
            }
        }

        result1 = await self.outbound_farm_repository.find_total_farms_and_hectares_by_farmer_id(farmer_id)
        data_for_chats["farm_count"] = result1["total_farms"]
        data_for_chats["total_hectares"] = result1["total_hectares"]

        result2 = await self.outbound_farm_repository.find_farm_counts_grouped_by_state_by_farmer_id(farmer_id)
        data_for_chats["farm_counts_grouped_by_state"] = result2

        result3 = await self.outbound_farm_repository.find_farm_grouped_by_state_by_farmer_id(farmer_id)
        data_for_chats["farms_grouped_by_state"] = result3

        result4 = await self.outbound_farm_repository.find_farms_count_grouped_by_culture_by_farmer_id(farmer_id)
        data_for_chats["farms_count_grouped_by_culture"] = result4

        result5 = await self.outbound_farm_repository.find_farms_grouped_by_culture_by_farmer_id(farmer_id)
        data_for_chats["farms_grouped_by_culture"] = result5

        result6 = await self.outbound_farm_repository.find_average_land_use_by_farmer_id(farmer_id)
        data_for_chats["average_land_use"]["average_arable_area"] = result6["average_arable_area"]
        data_for_chats["average_land_use"]["average_vegetation_area"] = result6["average_vegetation_area"]

        return data_for_chats

        