import pytest
from unittest.mock import AsyncMock

from adapters.outbound.outbound_culture_adapter import OutboundCultureAdapter

@pytest.mark.asyncio
class TestOutboundCultureAdapter:
    @pytest.fixture
    def mock_outbound_culture_repository_port(self):
        return AsyncMock()

    @pytest.fixture
    def culture_adapter(self, mock_outbound_culture_repository_port):
        return OutboundCultureAdapter(outbound_culture_repository_port=mock_outbound_culture_repository_port)

    @pytest.fixture
    def valid_culture(self):
        return {
            "name": "Cereal",
            "description": "A common crop culture",
        }

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_find_culture_by_id_success(self, culture_adapter, mock_outbound_culture_repository_port, trace_id):
        mock_outbound_culture_repository_port.find_culture_by_id.return_value = {
            "id": 1,
            "name": "Cereal",
            "description": "A common crop culture",
        }

        result = await culture_adapter.find_culture_by_id(1, trace_id)

        assert result["name"] == "Cereal"

        mock_outbound_culture_repository_port.find_culture_by_id.assert_called_once_with(1, trace_id)

    async def test_get_by_farmer_id_and_name_success(self, culture_adapter, mock_outbound_culture_repository_port, trace_id):
        mock_outbound_culture_repository_port.get_by_farmer_id_and_name.return_value = {
            "id": 1,
            "name": "Cereal",
            "description": "A common crop culture",
        }

        result = await culture_adapter.get_by_farmer_id_and_name(101, "Cereal", trace_id)

        assert result["name"] == "Cereal"

        mock_outbound_culture_repository_port.get_by_farmer_id_and_name.assert_called_once_with(101, "Cereal", trace_id)

    async def test_create_culture_for_a_farmer_success(self, culture_adapter, mock_outbound_culture_repository_port, valid_culture, trace_id):
        mock_outbound_culture_repository_port.create_culture_for_a_farmer.return_value = {
            "id": 1,
            "name": "Cereal",
            "description": "A common crop culture",
        }

        result = await culture_adapter.create_culture_for_a_farmer(101, valid_culture, trace_id)

        assert result["name"] == "Cereal"

        mock_outbound_culture_repository_port.create_culture_for_a_farmer.assert_called_once_with(101, valid_culture, trace_id)

    async def test_update_culture_by_id_success(self, culture_adapter, mock_outbound_culture_repository_port, valid_culture, trace_id):
        mock_outbound_culture_repository_port.update_culture_by_id.return_value = {
            "id": 1,
            "name": "Cereal Updated",
            "description": "An updated crop culture",
        }

        result = await culture_adapter.update_culture_by_id(1, valid_culture, trace_id)

        assert result["name"] == "Cereal Updated"

        mock_outbound_culture_repository_port.update_culture_by_id.assert_called_once_with(1, valid_culture, trace_id)
