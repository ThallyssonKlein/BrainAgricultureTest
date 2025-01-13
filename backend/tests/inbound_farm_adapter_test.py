import pytest
from unittest.mock import AsyncMock
from adapters.inbound.http.inbound_farm_adapter import InboundFarmAdapter
from domain.farm.farmer_not_found_error import FarmerNotFoundError
from ports.inbound.http.error.not_found_error import NotFoundError
from pydantic import BaseModel

class MockFarmSchema(BaseModel):
    name: str
    state: str
    arable_area: float
    vegetation_area: float

    def model_dump(self, *args, **kwargs):
        return super().model_dump(*args, **kwargs)


@pytest.mark.asyncio
class TestInboundFarmAdapter:
    @pytest.fixture
    def mock_adapters(self):
        return {
            "outbound_farm_repository_port": AsyncMock(),
            "farm_service": AsyncMock(),
        }

    @pytest.fixture
    def farm_adapter(self, mock_adapters):
        return InboundFarmAdapter(
            outbound_farm_repository_port=mock_adapters["outbound_farm_repository_port"],
            farm_service=mock_adapters["farm_service"],
        )

    @pytest.fixture
    def valid_farm(self):
        return MockFarmSchema(
            name="Sunny Farm",
            state="State A",
            arable_area=100.5,
            vegetation_area=50.3
        )

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_find_farms_by_state_and_farmer_id_success(self, farm_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_farm_repository_port"].find_farms_by_state_and_farmer_id.return_value = [
            {"id": 1, "name": "Farm A", "state": "State A"},
            {"id": 2, "name": "Farm B", "state": "State A"},
        ]

        result = await farm_adapter.find_farms_by_state_and_farmer_id(101, "State A", trace_id)

        assert len(result) == 2
        assert result[0]["name"] == "Farm A"

        mock_adapters["outbound_farm_repository_port"].find_farms_by_state_and_farmer_id.assert_called_once_with(
            101, "State A", trace_id
        )

    async def test_create_farm_for_a_farmer_success(self, farm_adapter, mock_adapters, valid_farm, trace_id):
        mock_adapters["farm_service"].create_farm_for_a_farmer.return_value = {
            "id": 1,
            "name": "Sunny Farm",
            "state": "State A",
            "arable_area": 100.5,
            "vegetation_area": 50.3,
        }

        result = await farm_adapter.create_farm_for_a_farmer(101, valid_farm, trace_id)

        assert result["name"] == "Sunny Farm"
        assert result["state"] == "State A"

        mock_adapters["farm_service"].create_farm_for_a_farmer.assert_called_once_with(
            101, valid_farm.model_dump(), trace_id
        )

    async def test_create_farm_farmer_not_found(self, farm_adapter, mock_adapters, valid_farm, trace_id):
        mock_adapters["farm_service"].create_farm_for_a_farmer.side_effect = FarmerNotFoundError

        with pytest.raises(NotFoundError, match="Farmer not found"):
            await farm_adapter.create_farm_for_a_farmer(101, valid_farm, trace_id)

    async def test_update_farm_success(self, farm_adapter, mock_adapters, valid_farm, trace_id):
        mock_adapters["outbound_farm_repository_port"].update_farm_by_id.return_value = {
            "id": 1,
            "name": "Sunny Farm Updated",
        }

        result = await farm_adapter.update_farm_by_id(1, valid_farm, trace_id)

        assert result["name"] == "Sunny Farm Updated"

        mock_adapters["outbound_farm_repository_port"].update_farm_by_id.assert_called_once_with(
            1, valid_farm.model_dump(), trace_id
        )

    async def test_update_farm_not_found(self, farm_adapter, mock_adapters, valid_farm, trace_id):
        mock_adapters["outbound_farm_repository_port"].update_farm_by_id.side_effect = ValueError("Farm not found")

        with pytest.raises(NotFoundError, match="Farm not found"):
            await farm_adapter.update_farm_by_id(1, valid_farm, trace_id)

    async def test_delete_farm_success(self, farm_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_farm_repository_port"].delete_farm_by_id.return_value = AsyncMock(rowcount=1)

        await farm_adapter.delete_farm_by_id(1, trace_id)

        mock_adapters["outbound_farm_repository_port"].delete_farm_by_id.assert_called_once_with(1, trace_id)

    async def test_delete_farm_not_found(self, farm_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_farm_repository_port"].delete_farm_by_id.return_value = AsyncMock(rowcount=0)

        with pytest.raises(NotFoundError, match="Farm not found"):
            await farm_adapter.delete_farm_by_id(1, trace_id)
