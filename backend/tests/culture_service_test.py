import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from domain.culture.culture_service import CultureService

@pytest.mark.asyncio
class TestCultureService:
    @pytest.fixture
    def mock_outbound_culture_adapter(self):
        return AsyncMock()

    @pytest.fixture
    def culture_service(self, mock_outbound_culture_adapter):
        return CultureService(outbound_culture_adapter=mock_outbound_culture_adapter)

    @pytest.fixture
    def valid_culture_data(self):
        return {"name": "Corn"}

    @pytest.fixture
    def update_culture_data(self):
        return {"name": "Wheat"}

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_culture_success(self, culture_service, mock_outbound_culture_adapter, valid_culture_data, trace_id):
        mock_outbound_culture_adapter.get_by_farmer_id_and_name.return_value = None
        mock_outbound_culture_adapter.create_culture_for_a_farmer.return_value = {
            "id": 1,
            "farmer_id": 101,
            "name": "Corn",
        }

        result = await culture_service.create_culture_for_a_farmer(101, valid_culture_data, trace_id)

        assert result["name"] == "Corn"
        assert result["farmer_id"] == 101

        mock_outbound_culture_adapter.get_by_farmer_id_and_name.assert_called_once_with(101, "Corn", trace_id)
        mock_outbound_culture_adapter.create_culture_for_a_farmer.assert_called_once_with(101, valid_culture_data, trace_id)

    async def test_create_culture_already_exists(self, culture_service, mock_outbound_culture_adapter, valid_culture_data, trace_id):
        mock_outbound_culture_adapter.get_by_farmer_id_and_name.return_value = {"id": 1, "name": "Corn"}

        with pytest.raises(CultureAlreadyExistsError):
            await culture_service.create_culture_for_a_farmer(101, valid_culture_data, trace_id)

        mock_outbound_culture_adapter.create_culture_for_a_farmer.assert_not_called()

    async def test_update_culture_success(self, culture_service, mock_outbound_culture_adapter, update_culture_data, trace_id):
        mock_outbound_culture_adapter.get_by_farmer_id_and_name.return_value = None
        mock_outbound_culture_adapter.update_culture_by_id.return_value = {
            "id": 1,
            "farmer_id": 101,
            "name": "Wheat",
        }

        result = await culture_service.update_culture_by_id(101, update_culture_data, trace_id)

        assert result["name"] == "Wheat"
        assert result["farmer_id"] == 101

        mock_outbound_culture_adapter.get_by_farmer_id_and_name.assert_called_once_with(101, "Wheat", trace_id)
        mock_outbound_culture_adapter.update_culture_by_id.assert_called_once_with(101, update_culture_data, trace_id)

    async def test_update_culture_already_exists(self, culture_service, mock_outbound_culture_adapter, update_culture_data, trace_id):
        mock_outbound_culture_adapter.get_by_farmer_id_and_name.return_value = {"id": 1, "name": "Wheat"}

        with pytest.raises(CultureAlreadyExistsError):
            await culture_service.update_culture_by_id(101, update_culture_data, trace_id)

        mock_outbound_culture_adapter.update_culture_by_id.assert_not_called()

    async def test_log_calls(self, culture_service, mock_outbound_culture_adapter, valid_culture_data, trace_id):
        mock_logger = MagicMock()
        culture_service.log = mock_logger

        mock_outbound_culture_adapter.get_by_farmer_id_and_name.return_value = None
        mock_outbound_culture_adapter.create_culture_for_a_farmer.return_value = {
            "id": 1,
            "farmer_id": 101,
            "name": "Corn",
        }

        await culture_service.create_culture_for_a_farmer(101, valid_culture_data, trace_id)

        mock_logger.info.assert_any_call(f"Creating culture for farmer with id: 101 and data: {valid_culture_data}", trace_id)
