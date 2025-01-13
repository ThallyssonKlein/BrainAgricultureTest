import pytest
from unittest.mock import AsyncMock
from adapters.inbound.http.inbound_dashboard_adapter import InboundDashboardAdapter

@pytest.mark.asyncio
class TestInboundDashboardAdapter:
    @pytest.fixture
    def mock_outbound_farm_repository(self):
        return AsyncMock()

    @pytest.fixture
    def dashboard_adapter(self, mock_outbound_farm_repository):
        return InboundDashboardAdapter(outbound_farm_repository=mock_outbound_farm_repository)

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_get_dashboard_data_success(self, dashboard_adapter, mock_outbound_farm_repository, trace_id):
        farmer_id = 101

        mock_outbound_farm_repository.find_total_farms_and_hectares_by_farmer_id.return_value = {
            "farm_count": 5,
            "total_hectares": 200,
        }
        mock_outbound_farm_repository.find_farm_counts_grouped_by_state_by_farmer_id.return_value = [
            {"state": "State A", "count": 3},
            {"state": "State B", "count": 2},
        ]
        mock_outbound_farm_repository.find_farms_count_grouped_by_culture_by_farmer_id.return_value = [
            {"culture": "Wheat", "count": 4},
            {"culture": "Corn", "count": 1},
        ]
        mock_outbound_farm_repository.find_average_land_use_by_farmer_id.return_value = {
            "average_arable_area": 100,
            "average_vegetation_area": 50,
        }

        result = await dashboard_adapter.get_dashboard_data(farmer_id, trace_id)

        assert result["farm_count"] == 5
        assert result["total_hectares"] == 200
        assert result["farm_counts_grouped_by_state"] == [
            {"state": "State A", "count": 3},
            {"state": "State B", "count": 2},
        ]
        assert result["farms_count_grouped_by_culture"] == [
            {"culture": "Wheat", "count": 4},
            {"culture": "Corn", "count": 1},
        ]
        assert result["average_land_use"] == {
            "average_arable_area": 100,
            "average_vegetation_area": 50,
        }

        mock_outbound_farm_repository.find_total_farms_and_hectares_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
        mock_outbound_farm_repository.find_farm_counts_grouped_by_state_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
        mock_outbound_farm_repository.find_farms_count_grouped_by_culture_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
        mock_outbound_farm_repository.find_average_land_use_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )

    async def test_get_dashboard_data_empty_results(self, dashboard_adapter, mock_outbound_farm_repository, trace_id):
        farmer_id = 102

        mock_outbound_farm_repository.find_total_farms_and_hectares_by_farmer_id.return_value = {
            "farm_count": 0,
            "total_hectares": 0,
        }
        mock_outbound_farm_repository.find_farm_counts_grouped_by_state_by_farmer_id.return_value = []
        mock_outbound_farm_repository.find_farms_count_grouped_by_culture_by_farmer_id.return_value = []
        mock_outbound_farm_repository.find_average_land_use_by_farmer_id.return_value = {
            "average_arable_area": 0,
            "average_vegetation_area": 0,
        }

        result = await dashboard_adapter.get_dashboard_data(farmer_id, trace_id)

        assert result["farm_count"] == 0
        assert result["total_hectares"] == 0
        assert result["farm_counts_grouped_by_state"] == []
        assert result["farms_count_grouped_by_culture"] == []
        assert result["average_land_use"] == {
            "average_arable_area": 0,
            "average_vegetation_area": 0,
        }

        mock_outbound_farm_repository.find_total_farms_and_hectares_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
        mock_outbound_farm_repository.find_farm_counts_grouped_by_state_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
        mock_outbound_farm_repository.find_farms_count_grouped_by_culture_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
        mock_outbound_farm_repository.find_average_land_use_by_farmer_id.assert_called_once_with(
            farmer_id, trace_id
        )
