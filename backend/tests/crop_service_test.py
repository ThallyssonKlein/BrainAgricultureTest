import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.crop.crop_service import CropService
from domain.crop.culture_not_found_error import CultureNotFoundError
from domain.crop.farm_not_found_error import FarmNotFoundError

@pytest.mark.asyncio
class TestCropService:
    @pytest.fixture
    def mock_adapters(self):
        return {
            "outbound_crop_adapter": AsyncMock(),
            "outbound_culture_adapter": AsyncMock(),
            "outbound_farm_adapter": AsyncMock(),
        }

    @pytest.fixture
    def crop_service(self, mock_adapters):
        return CropService(
            outbound_crop_adapter=mock_adapters["outbound_crop_adapter"],
            outbound_culture_adapter=mock_adapters["outbound_culture_adapter"],
            outbound_farm_adapter=mock_adapters["outbound_farm_adapter"],
        )

    @pytest.fixture
    def valid_culture(self):
        return {"id": 1, "name": "Corn"}

    @pytest.fixture
    def valid_farm(self):
        return {"id": 101, "name": "Farm A"}

    @pytest.fixture
    def crop_data(self):
        return {"culture": {"id": 1}, "details": "Planting details"}

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_crop_success(self, crop_service, mock_adapters, valid_culture, valid_farm, crop_data, trace_id):
        """Teste para criação de uma safra com cultura e fazenda válidas."""
        mock_adapters["outbound_culture_adapter"].find_culture_by_id.return_value = valid_culture
        mock_adapters["outbound_farm_adapter"].find_farm_by_id.return_value = valid_farm
        mock_adapters["outbound_crop_adapter"].create_crop_for_a_farm_and_return_with_culture.return_value = {
            "id": 1,
            "farm_id": 101,
            "culture": valid_culture,
            "details": crop_data["details"],
        }

        result = await crop_service.create_crop_for_a_farm_and_return_culture(101, crop_data, trace_id)

        assert result["farm_id"] == 101
        assert result["culture"] == valid_culture
        assert result["details"] == crop_data["details"]

        mock_adapters["outbound_culture_adapter"].find_culture_by_id.assert_called_once_with(1, trace_id)
        mock_adapters["outbound_farm_adapter"].find_farm_by_id.assert_called_once_with(101, trace_id)
        mock_adapters["outbound_crop_adapter"].create_crop_for_a_farm_and_return_with_culture.assert_called_once_with(
            101, crop_data, trace_id
        )

    async def test_culture_not_found(self, crop_service, mock_adapters, crop_data, trace_id):
        """Teste para exceção quando a cultura não é encontrada."""
        mock_adapters["outbound_culture_adapter"].find_culture_by_id.return_value = None

        with pytest.raises(CultureNotFoundError):
            await crop_service.create_crop_for_a_farm_and_return_culture(101, crop_data, trace_id)

        mock_adapters["outbound_farm_adapter"].find_farm_by_id.assert_not_called()
        mock_adapters["outbound_crop_adapter"].create_crop_for_a_farm_and_return_with_culture.assert_not_called()

    async def test_farm_not_found(self, crop_service, mock_adapters, valid_culture, crop_data, trace_id):
        """Teste para exceção quando a fazenda não é encontrada."""
        mock_adapters["outbound_culture_adapter"].find_culture_by_id.return_value = valid_culture
        mock_adapters["outbound_farm_adapter"].find_farm_by_id.return_value = None

        with pytest.raises(FarmNotFoundError):
            await crop_service.create_crop_for_a_farm_and_return_culture(101, crop_data, trace_id)

        mock_adapters["outbound_culture_adapter"].find_culture_by_id.assert_called_once_with(1, trace_id)
        mock_adapters["outbound_crop_adapter"].create_crop_for_a_farm_and_return_with_culture.assert_not_called()

    async def test_log_calls(self, crop_service, mock_adapters, valid_culture, valid_farm, crop_data, trace_id):
        """Teste para verificar chamadas de log em diferentes cenários."""
        mock_logger = MagicMock()
        crop_service.log = mock_logger

        mock_adapters["outbound_culture_adapter"].find_culture_by_id.return_value = valid_culture
        mock_adapters["outbound_farm_adapter"].find_farm_by_id.return_value = valid_farm
        mock_adapters["outbound_crop_adapter"].create_crop_for_a_farm_and_return_with_culture.return_value = {
            "id": 1,
            "farm_id": 101,
            "culture": valid_culture,
            "details": crop_data["details"],
        }

        await crop_service.create_crop_for_a_farm_and_return_culture(101, crop_data, trace_id)

        mock_logger.info.assert_any_call(f"Validating culture with id: {crop_data['culture']['id']}", trace_id)
        mock_logger.info.assert_any_call(f"Validating farm with id: 101", trace_id)
        mock_logger.info.assert_any_call(f"Creating crop for farm with id: 101 and data: {crop_data}", trace_id)
