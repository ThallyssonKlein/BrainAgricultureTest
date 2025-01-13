import pytest
from unittest.mock import AsyncMock

from adapters.outbound.outbound_crop_adapter import OutboundCropAdapter

@pytest.mark.asyncio
class TestOutboundCropAdapter:
    @pytest.fixture
    def mock_outbound_crop_repository_port(self):
        return AsyncMock()

    @pytest.fixture
    def crop_adapter(self, mock_outbound_crop_repository_port):
        return OutboundCropAdapter(outbound_crop_repository_port=mock_outbound_crop_repository_port)

    @pytest.fixture
    def valid_crop(self):
        return {
            "name": "Corn",
            "variety": "Sweet Corn",
            "quantity": 100,
            "culture_id": 1,
        }

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_crop_success(self, crop_adapter, mock_outbound_crop_repository_port, valid_crop, trace_id):
        mock_outbound_crop_repository_port.create_crop_for_a_farm_and_return_with_culture.return_value = {
            "id": 1,
            "name": "Corn",
            "variety": "Sweet Corn",
            "quantity": 100,
            "culture": {"id": 1, "name": "Cereal"},
        }

        result = await crop_adapter.create_crop_for_a_farm_and_return_with_culture(101, valid_crop, trace_id)

        assert result["name"] == "Corn"
        assert result["variety"] == "Sweet Corn"
        assert result["quantity"] == 100
        assert result["culture"]["name"] == "Cereal"

        mock_outbound_crop_repository_port.create_crop_for_a_farm_and_return_with_culture.assert_called_once_with(
            101, valid_crop, trace_id
        )

    async def test_create_crop_error(self, crop_adapter, mock_outbound_crop_repository_port, valid_crop, trace_id):
        mock_outbound_crop_repository_port.create_crop_for_a_farm_and_return_with_culture.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await crop_adapter.create_crop_for_a_farm_and_return_with_culture(101, valid_crop, trace_id)

        mock_outbound_crop_repository_port.create_crop_for_a_farm_and_return_with_culture.assert_called_once_with(
            101, valid_crop, trace_id
        )
