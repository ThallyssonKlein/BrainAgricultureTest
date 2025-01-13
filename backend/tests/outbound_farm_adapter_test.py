import pytest
from unittest.mock import AsyncMock

from adapters.outbound.outbound_farm_adapter import OutboundFarmAdapter

@pytest.mark.asyncio
class TestOutboundFarmAdapter:
    @pytest.fixture
    def mock_outbound_farm_repository_port(self):
        return AsyncMock()

    @pytest.fixture
    def farm_adapter(self, mock_outbound_farm_repository_port):
        return OutboundFarmAdapter(outbound_farm_repository_port=mock_outbound_farm_repository_port)

    @pytest.fixture
    def valid_farm(self):
        return {
            "name": "Sunny Farm",
            "location": "State A",
            "arable_area": 100.5,
            "vegetation_area": 50.3,
        }

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_find_farm_by_id_success(self, farm_adapter, mock_outbound_farm_repository_port, trace_id):
        mock_outbound_farm_repository_port.find_farm_by_id.return_value = {
            "id": 1,
            "name": "Sunny Farm",
            "location": "State A",
            "arable_area": 100.5,
            "vegetation_area": 50.3,
        }

        result = await farm_adapter.find_farm_by_id(1, trace_id)

        assert result["name"] == "Sunny Farm"
        assert result["location"] == "State A"

        mock_outbound_farm_repository_port.find_farm_by_id.assert_called_once_with(1, trace_id)

    async def test_find_farm_by_id_not_found(self, farm_adapter, mock_outbound_farm_repository_port, trace_id):
        mock_outbound_farm_repository_port.find_farm_by_id.return_value = None

        result = await farm_adapter.find_farm_by_id(999, trace_id)

        assert result is None

        mock_outbound_farm_repository_port.find_farm_by_id.assert_called_once_with(999, trace_id)

    async def test_create_farm_for_a_farmer_success(self, farm_adapter, mock_outbound_farm_repository_port, valid_farm, trace_id):
        mock_outbound_farm_repository_port.create_farm_for_a_farmer.return_value = {
            "id": 1,
            "name": "Sunny Farm",
            "location": "State A",
            "arable_area": 100.5,
            "vegetation_area": 50.3,
        }

        result = await farm_adapter.create_farm_for_a_farmer(101, valid_farm, trace_id)

        assert result["name"] == "Sunny Farm"
        assert result["location"] == "State A"

        mock_outbound_farm_repository_port.create_farm_for_a_farmer.assert_called_once_with(101, valid_farm, trace_id)

    async def test_create_farm_for_a_farmer_error(self, farm_adapter, mock_outbound_farm_repository_port, valid_farm, trace_id):
        mock_outbound_farm_repository_port.create_farm_for_a_farmer.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await farm_adapter.create_farm_for_a_farmer(101, valid_farm, trace_id)

        mock_outbound_farm_repository_port.create_farm_for_a_farmer.assert_called_once_with(101, valid_farm, trace_id)
