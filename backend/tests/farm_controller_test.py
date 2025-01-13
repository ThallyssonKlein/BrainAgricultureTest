import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from adapters.inbound.http.schemas import FarmSchema
from ports.inbound.http.controllers.farm_controller import FarmController

@pytest.fixture
def mock_farm_adapter():
    return AsyncMock()

@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.state.trace_id = "trace-12345"
    return request

@pytest.fixture
def farm_controller(mock_farm_adapter):
    return FarmController(inbound_farm_adapter=mock_farm_adapter)

@pytest.mark.asyncio
async def test_find_farms_by_state(farm_controller, mock_farm_adapter, mock_request):
    farmer_id = 1
    state = "SP"
    farms = [{"id": 1, "name": "Farm 1"}, {"id": 2, "name": "Farm 2"}]

    mock_farm_adapter.find_farms_by_state_and_farmer_id.return_value = farms

    result = await farm_controller.find_farm_by_farmer_id_and_state(mock_request, farmer_id, state)

    assert result == farms
    mock_farm_adapter.find_farms_by_state_and_farmer_id.assert_called_once_with(farmer_id, state, "trace-12345")

@pytest.mark.asyncio
async def test_find_farms_ordered_by_vegetation_area_desc(farm_controller, mock_farm_adapter, mock_request):
    farmer_id = 1
    farms = [{"id": 1, "name": "Farm A"}, {"id": 2, "name": "Farm B"}]

    mock_farm_adapter.find_farms_ordered_by_vegetation_area_desc_by_farmer_id.return_value = farms

    result = await farm_controller.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(mock_request, farmer_id)

    assert result == farms
    mock_farm_adapter.find_farms_ordered_by_vegetation_area_desc_by_farmer_id.assert_called_once_with(farmer_id, "trace-12345")

@pytest.mark.asyncio
async def test_find_farms_ordered_by_arable_area_desc(farm_controller, mock_farm_adapter, mock_request):
    farmer_id = 1
    farms = [{"id": 1, "name": "Farm A"}, {"id": 2, "name": "Farm B"}]

    mock_farm_adapter.find_farms_ordered_by_arable_area_desc_by_farmer_id.return_value = farms

    result = await farm_controller.find_farms_ordered_by_arable_area_desc_by_farmer_id(mock_request, farmer_id)

    assert result == farms
    mock_farm_adapter.find_farms_ordered_by_arable_area_desc_by_farmer_id.assert_called_once_with(farmer_id, "trace-12345")

@pytest.mark.asyncio
async def test_create_farm_for_a_farmer(farm_controller, mock_farm_adapter, mock_request):
    farmer_id = 1
    farm_data = FarmSchema(
        name="Farm A",
        arable_area=100.0,
        vegetation_area=50.0,
        city="City A",
        state="SP",
    )
    created_farm = {"id": 1, "name": "Farm A"}

    mock_farm_adapter.create_farm_for_a_farmer.return_value = created_farm

    result = await farm_controller.create_farm_for_a_farmer(mock_request, farmer_id, farm_data)

    assert result == created_farm
    mock_farm_adapter.create_farm_for_a_farmer.assert_called_once_with(farmer_id, farm_data, "trace-12345")

@pytest.mark.asyncio
async def test_update_farm_by_id(farm_controller, mock_farm_adapter, mock_request):
    farm_id = 1
    farm_data = FarmSchema(
        name="Farm A",
        arable_area=100.0,
        vegetation_area=50.0,
        city="City A",
        state="SP",
    )
    updated_farm = {"id": 1, "name": "Farm A - Updated"}

    mock_farm_adapter.update_farm_by_id.return_value = updated_farm

    result = await farm_controller.update_farm_by_id(mock_request, farm_id, farm_data)

    assert result == updated_farm
    mock_farm_adapter.update_farm_by_id.assert_called_once_with(farm_id, farm_data, "trace-12345")

@pytest.mark.asyncio
async def test_delete_farm_by_id(farm_controller, mock_farm_adapter, mock_request):
    farm_id = 1

    result = await farm_controller.delete_farm_by_id(mock_request, farm_id)

    assert result == {"message": "Farm deleted"}
    mock_farm_adapter.delete_farm_by_id.assert_called_once_with(farm_id, "trace-12345")

@pytest.mark.asyncio
async def test_find_farms_invalid_parameters(farm_controller, mock_request):
    farmer_id = 1
    mock_request.state.trace_id = "trace-12345"

    result = await farm_controller.find_farms(mock_request, farmer_id, state=None, order_by="invalid")

    assert result == {"error": "Invalid parameters"}
