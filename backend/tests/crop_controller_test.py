import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from datetime import date
from adapters.inbound.http.schemas import CropSchema, ResumedCultureSchema
from ports.inbound.http.controllers.crop_controller import CropController

@pytest.fixture
def mock_inbound_crop_adapter():
    return AsyncMock()


@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.state.trace_id = "trace-12345"
    return request


@pytest.fixture
def crop_controller(mock_inbound_crop_adapter):
    return CropController(inbound_crop_adapter=mock_inbound_crop_adapter)

@pytest.mark.asyncio
async def test_create_crop_for_a_farm_and_return_culture(crop_controller, mock_inbound_crop_adapter, mock_request):
    farm_id = 1
    crop_data = CropSchema(
        date=date(2025, 1, 1),
        culture=ResumedCultureSchema(id=1)
    )
    crop_response = {
        "id": 1,
        "date": "2025-01-01",
        "culture": {"id": 1}
    }
    mock_inbound_crop_adapter.create_crop_for_a_farm_and_return_culture.return_value = crop_response

    result = await crop_controller.create_crop_for_a_farm_and_return_culture(
        mock_request,
        farm_id=farm_id,
        crop=crop_data
    )

    assert result == crop_response
    mock_inbound_crop_adapter.create_crop_for_a_farm_and_return_culture.assert_called_once_with(
        farm_id, crop_data, "trace-12345"
    )


@pytest.mark.asyncio
async def test_find_crops(crop_controller, mock_inbound_crop_adapter, mock_request):
    culture_name = "Wheat"
    farmer_id = 123
    crops_response = [
        {"id": 1, "date": "2025-01-01", "culture": {"id": 1}},
        {"id": 2, "date": "2025-02-01", "culture": {"id": 2}},
    ]
    mock_inbound_crop_adapter.find_crops.return_value = crops_response

    result = await crop_controller.find_crops(mock_request, culture_name=culture_name, farmer_id=farmer_id)

    assert result == crops_response
    mock_inbound_crop_adapter.find_crops.assert_called_once_with(culture_name, farmer_id, "trace-12345")


@pytest.mark.asyncio
async def test_update_crop_by_id(crop_controller, mock_inbound_crop_adapter, mock_request):
    crop_id = 1
    crop_data = CropSchema(
        date=date(2025, 1, 1),
        culture=ResumedCultureSchema(id=1)
    )
    updated_crop_response = {
        "id": 1,
        "date": "2025-01-01",
        "culture": {"id": 1}
    }
    mock_inbound_crop_adapter.update_crop_by_id.return_value = updated_crop_response

    result = await crop_controller.update_crop_by_id(mock_request, crop_id=crop_id, crop=crop_data)

    assert result == updated_crop_response
    mock_inbound_crop_adapter.update_crop_by_id.assert_called_once_with(
        crop_id, crop_data, "trace-12345"
    )


@pytest.mark.asyncio
async def test_delete_crop_by_id(crop_controller, mock_inbound_crop_adapter, mock_request):
    crop_id = 1
    mock_inbound_crop_adapter.delete_crop_by_id.return_value = None

    result = await crop_controller.delete_crop_by_id(mock_request, crop_id=crop_id)

    assert result is None
    mock_inbound_crop_adapter.delete_crop_by_id.assert_called_once_with(crop_id, "trace-12345")
