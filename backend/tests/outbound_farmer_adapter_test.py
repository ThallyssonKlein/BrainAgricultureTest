import pytest
from unittest.mock import AsyncMock

from adapters.outbound.outbound_farmer_adapter import OutboundFarmerAdapter

@pytest.mark.asyncio
class TestOutboundFarmerAdapter:
    @pytest.fixture
    def mock_outbound_farmer_repository_port(self):
        return AsyncMock()

    @pytest.fixture
    def farmer_adapter(self, mock_outbound_farmer_repository_port):
        return OutboundFarmerAdapter(outbound_farmer_repository_port=mock_outbound_farmer_repository_port)

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_find_farmer_by_id_success(self, farmer_adapter, mock_outbound_farmer_repository_port, trace_id):
        mock_outbound_farmer_repository_port.find_farmer_by_id.return_value = {
            "id": 1,
            "name": "John Doe",
            "document": "12345678901",
        }

        result = await farmer_adapter.find_farmer_by_id(1, trace_id)

        assert result["name"] == "John Doe"
        assert result["document"] == "12345678901"

        mock_outbound_farmer_repository_port.find_farmer_by_id.assert_called_once_with(1, trace_id)

    async def test_find_farmer_by_id_not_found(self, farmer_adapter, mock_outbound_farmer_repository_port, trace_id):
        mock_outbound_farmer_repository_port.find_farmer_by_id.return_value = None

        result = await farmer_adapter.find_farmer_by_id(999, trace_id)

        assert result is None

        mock_outbound_farmer_repository_port.find_farmer_by_id.assert_called_once_with(999, trace_id)

    async def test_find_farmer_by_id_error(self, farmer_adapter, mock_outbound_farmer_repository_port, trace_id):
        mock_outbound_farmer_repository_port.find_farmer_by_id.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await farmer_adapter.find_farmer_by_id(1, trace_id)

        mock_outbound_farmer_repository_port.find_farmer_by_id.assert_called_once_with(1, trace_id)
