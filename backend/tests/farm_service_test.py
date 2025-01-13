import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.farm.farm_service import FarmService
from domain.farm.farmer_not_found_error import FarmerNotFoundError

@pytest.mark.asyncio
class TestFarmService:
    @pytest.fixture
    def mock_adapters(self):
        return {
            "outbound_farm_adapter": AsyncMock(),
            "outbound_farmer_adapter": AsyncMock(),
        }

    @pytest.fixture
    def farm_service(self, mock_adapters):
        return FarmService(
            outbound_farm_adapter=mock_adapters["outbound_farm_adapter"],
            outbound_farmer_adapter=mock_adapters["outbound_farmer_adapter"],
        )

    @pytest.fixture
    def valid_farm_data(self):
        return {
            "name": "Sunny Farm",
            "arable_area": 100.0,
            "vegetation_area": 50.0,
            "city": "Green Valley",
            "state": "SP",
        }

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_farm_success(self, farm_service, mock_adapters, valid_farm_data, trace_id):
        mock_adapters["outbound_farmer_adapter"].find_farmer_by_id.return_value = {"id": 1, "name": "John Doe"}
        returnValue = {
            "id": 1,
            "farmer_id": 1,
            "name": "Sunny Farm",
            "arable_area": 100.0,
            "vegetation_area": 50.0,
            "city": "Green Valley",
            "state": "SP",   
        }
        mock_adapters["outbound_farm_adapter"].create_farm_for_a_farmer.return_value = returnValue

        result = await farm_service.create_farm_for_a_farmer(1, valid_farm_data, trace_id)

        assert result == returnValue

        mock_adapters["outbound_farmer_adapter"].find_farmer_by_id.assert_called_once_with(1, trace_id)
        mock_adapters["outbound_farm_adapter"].create_farm_for_a_farmer.assert_called_once_with(1, valid_farm_data, trace_id)

    async def test_create_farm_farmer_not_found(self, farm_service, mock_adapters, valid_farm_data, trace_id):
        mock_adapters["outbound_farmer_adapter"].find_farmer_by_id.return_value = None

        with pytest.raises(FarmerNotFoundError):
            await farm_service.create_farm_for_a_farmer(1, valid_farm_data, trace_id)

        mock_adapters["outbound_farm_adapter"].create_farm_for_a_farmer.assert_not_called()

    async def test_log_calls(self, farm_service, mock_adapters, valid_farm_data, trace_id):
        mock_logger = MagicMock()
        farm_service.log = mock_logger

        mock_adapters["outbound_farmer_adapter"].find_farmer_by_id.return_value = {"id": 1, "name": "John Doe"}
        mock_adapters["outbound_farm_adapter"].create_farm_for_a_farmer.return_value = {
            "id": 101,
            "farmer_id": 1,
            "name": "Sunny Farm",
            "location": "Green Valley",
        }

        await farm_service.create_farm_for_a_farmer(1, valid_farm_data, trace_id)

        mock_logger.info.assert_any_call(f"Finding farmer with id: 1", trace_id)
        mock_logger.info.assert_any_call(f"Creating farm for farmer with id: 1 and data: {valid_farm_data}", trace_id)
