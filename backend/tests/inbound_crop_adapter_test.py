import pytest
from unittest.mock import AsyncMock
from domain.crop.culture_not_found_error import CultureNotFoundError
from domain.crop.farm_not_found_error import FarmNotFoundError
from ports.inbound.http.error.bad_request_error import BadRequestError
from ports.inbound.http.error.not_found_error import NotFoundError
from adapters.inbound.http.inbound_crop_adapter import InboundCropAdapter
from pydantic import BaseModel

class MockCropSchema(BaseModel):
    date: str
    culture: dict

    def model_dump(self, *args, **kwargs):
        return super().model_dump(*args, **kwargs)

class Result:
    def __init__(self, rowcount=0):
        self.rowcount = rowcount

@pytest.mark.asyncio
class TestInboundCropAdapter:
    @pytest.fixture
    def mock_adapters(self):
        return {
            "outbound_crop_repository_port": AsyncMock(),
            "crop_service": AsyncMock(),
        }

    @pytest.fixture
    def inbound_crop_adapter(self, mock_adapters):
        return InboundCropAdapter(
            outbound_crop_repository_port=mock_adapters["outbound_crop_repository_port"],
            crop_service=mock_adapters["crop_service"],
        )

    @pytest.fixture
    def valid_crop(self):
        return MockCropSchema(date="2021-01-01", culture={"id": 1, "name": "Cereal"})

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_crop_success(self, inbound_crop_adapter, mock_adapters, valid_crop, trace_id):
        returnValue = {
            "id": 1,
            "date": "2021-01-01",
            "culture": {"id": 1, "name": "Cereal"},
        }
        mock_adapters["crop_service"].create_crop_for_a_farm_and_return_culture.return_value = returnValue

        result = await inbound_crop_adapter.create_crop_for_a_farm_and_return_culture(101, valid_crop, trace_id)

        assert result == returnValue

        mock_adapters["crop_service"].create_crop_for_a_farm_and_return_culture.assert_called_once_with(
            101, valid_crop.model_dump(), trace_id
        )

    async def test_create_crop_culture_not_found(self, inbound_crop_adapter, mock_adapters, valid_crop, trace_id):
        mock_adapters["crop_service"].create_crop_for_a_farm_and_return_culture.side_effect = CultureNotFoundError

        with pytest.raises(NotFoundError, match="Culture not found"):
            await inbound_crop_adapter.create_crop_for_a_farm_and_return_culture(101, valid_crop, trace_id)
    
    async def test_create_farm_not_found(self, inbound_crop_adapter, mock_adapters, valid_crop, trace_id):
        mock_adapters["crop_service"].create_crop_for_a_farm_and_return_culture.side_effect = FarmNotFoundError

        with pytest.raises(NotFoundError, match="Farm not found"):
            await inbound_crop_adapter.create_crop_for_a_farm_and_return_culture(101, valid_crop, trace_id)

    async def test_update_crop_success(self, inbound_crop_adapter, mock_adapters, valid_crop, trace_id):
        mock_adapters["outbound_crop_repository_port"].update_crop_by_id.return_value = {"id": 1, "name": "Wheat"}

        result = await inbound_crop_adapter.update_crop_by_id(1, valid_crop, trace_id)

        assert result["name"] == "Wheat"

        mock_adapters["outbound_crop_repository_port"].update_crop_by_id.assert_called_once_with(
            1, valid_crop.model_dump(), trace_id
        )

    async def test_update_crop_not_found(self, inbound_crop_adapter, mock_adapters, valid_crop, trace_id):
        mock_adapters["outbound_crop_repository_port"].update_crop_by_id.side_effect = ValueError("Crop not found")

        with pytest.raises(NotFoundError, match="Crop not found"):
            await inbound_crop_adapter.update_crop_by_id(1, valid_crop, trace_id)
    
    async def test_delete_crop_by_id_success(self, inbound_crop_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_crop_repository_port"].delete_crop_by_id.return_value = Result(rowcount=1)

        await inbound_crop_adapter.delete_crop_by_id(1, trace_id)

        mock_adapters["outbound_crop_repository_port"].delete_crop_by_id.assert_called_once_with(1, trace_id)
    
    async def test_delete_crop_by_id_crop_not_found(self, inbound_crop_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_crop_repository_port"].delete_crop_by_id.return_value = Result()

        with pytest.raises(NotFoundError, match="Crop not found"):
            await inbound_crop_adapter.delete_crop_by_id(1, trace_id)
    
    async def test_find_crops_with_culture_name_and_farmer_id_success(self, inbound_crop_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_crop_repository_port"].find_crops_by_culture_name_and_farmer_id.return_value = [
            {"id": 1, "date": "2025-01-01", "culture": {"id": 1}},
            {"id": 2, "date": "2025-02-01", "culture": {"id": 2}},
        ]

        result = await inbound_crop_adapter.find_crops("Wheat", 123, trace_id)

        assert result == [
            {"id": 1, "date": "2025-01-01", "culture": {"id": 1}},
            {"id": 2, "date": "2025-02-01", "culture": {"id": 2}},
        ]

        mock_adapters["outbound_crop_repository_port"].find_crops_by_culture_name_and_farmer_id.assert_called_once_with(
            "Wheat", 123, trace_id
        )

    async def test_find_crops_with_invalid_parameters(self, inbound_crop_adapter, mock_adapters, trace_id):
        with pytest.raises(BadRequestError, match="Invalid query parameters"):
            await inbound_crop_adapter.find_crops(None, None, trace_id)
