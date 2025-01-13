import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from adapters.inbound.http.schemas import CultureSchema
from ports.inbound.http.controllers.culture_controller import CultureController

@pytest.fixture
def mock_inbound_culture_adapter():
    return AsyncMock()

@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.state.trace_id = "trace-12345"
    return request


@pytest.fixture
def culture_controller(mock_inbound_culture_adapter):
    return CultureController(inbound_culture_adapter=mock_inbound_culture_adapter)

@pytest.mark.asyncio
async def test_create_a_culture_for_a_farmer(culture_controller, mock_inbound_culture_adapter, mock_request):
    farmer_id = 1
    culture_data = CultureSchema(name="Cereal")
    created_culture_response = {"id": 1, "name": "Cereal"}

    mock_inbound_culture_adapter.create_culture_for_a_farmer.return_value = created_culture_response

    result = await culture_controller.create_a_culture_for_a_farmer(
        mock_request,
        farmer_id=farmer_id,
        culture=culture_data
    )

    assert result == created_culture_response
    mock_inbound_culture_adapter.create_culture_for_a_farmer.assert_called_once_with(
        farmer_id, culture_data, "trace-12345"
    )


@pytest.mark.asyncio
async def test_get_cultures_for_a_farmer(culture_controller, mock_inbound_culture_adapter, mock_request):
    farmer_id = 1
    cultures_response = [
        {"id": 1, "name": "Cereal"},
        {"id": 2, "name": "Legume"}
    ]

    mock_inbound_culture_adapter.get_cultures_for_a_farmer.return_value = cultures_response

    result = await culture_controller.get_cultures_for_a_farmer(mock_request, farmer_id=farmer_id)

    assert result == cultures_response
    mock_inbound_culture_adapter.get_cultures_for_a_farmer.assert_called_once_with(farmer_id, "trace-12345")


@pytest.mark.asyncio
async def test_update_culture_by_id(culture_controller, mock_inbound_culture_adapter, mock_request):
    culture_id = 1
    culture_data = CultureSchema(name="Updated Cereal")
    updated_culture_response = {"id": 1, "name": "Updated Cereal"}

    mock_inbound_culture_adapter.update_culture_by_id.return_value = updated_culture_response

    result = await culture_controller.update_culture_by_id(
        mock_request,
        culture_id=culture_id,
        culture=culture_data
    )

    assert result == updated_culture_response
    mock_inbound_culture_adapter.update_culture_by_id.assert_called_once_with(
        culture_id, culture_data, "trace-12345"
    )


@pytest.mark.asyncio
async def test_delete_culture_by_id(culture_controller, mock_inbound_culture_adapter, mock_request):
    culture_id = 1
    mock_inbound_culture_adapter.delete_culture_by_id.return_value = None

    result = await culture_controller.delete_culture_by_id(mock_request, culture_id=culture_id)

    assert result is None
    mock_inbound_culture_adapter.delete_culture_by_id.assert_called_once_with(culture_id, "trace-12345")
