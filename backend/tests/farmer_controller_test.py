import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.controllers.farmer_controller import FarmerController
from ports.inbound.http.error.bad_request_error import BadRequestError

@pytest.fixture
def mock_farmer_adapter():
    return AsyncMock()

@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.state.trace_id = "trace-12345"
    return request

@pytest.fixture
def farmer_controller(mock_farmer_adapter):
    return FarmerController(farmer_adapter=mock_farmer_adapter)

@pytest.mark.asyncio
async def test_create_farmer(farmer_controller, mock_farmer_adapter, mock_request):
    farmer_data = FarmerSchema(
        document="12345678901",
        name="John Doe",
        city="City A",
        state="SP"
    )
    created_farmer = {"id": 1, "name": "John Doe"}

    mock_farmer_adapter.create_farmer.return_value = created_farmer

    result = await farmer_controller.create_farmer(mock_request, farmer_data)

    assert result == created_farmer
    mock_farmer_adapter.create_farmer.assert_called_once_with(farmer_data, "trace-12345")

@pytest.mark.asyncio
async def test_update_farmer_by_id(farmer_controller, mock_farmer_adapter, mock_request):
    farmer_id = 1
    farmer_data = FarmerSchema(
        document="12345678901",
        name="John Doe Updated",
        city="City B",
        state="RJ"
    )
    updated_farmer = {"id": 1, "name": "John Doe Updated"}

    mock_farmer_adapter.update_farmer.return_value = updated_farmer

    result = await farmer_controller.update_farmer_by_id(mock_request, farmer_id, farmer_data)

    assert result == updated_farmer
    mock_farmer_adapter.update_farmer.assert_called_once_with(farmer_id, farmer_data, "trace-12345")

@pytest.mark.asyncio
async def test_find_farmers_paginated_and_with_query(farmer_controller, mock_farmer_adapter, mock_request):
    limit = 10
    page = 1
    query = "John"
    farmers = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "John Smith"}]

    mock_farmer_adapter.find_farmers_paginated_and_with_query.return_value = farmers

    result = await farmer_controller.find_farmers_paginated_and_with_query(mock_request, limit, page, query)

    assert result == farmers
    mock_farmer_adapter.find_farmers_paginated_and_with_query.assert_called_once_with(limit, page, query, "trace-12345")

@pytest.mark.asyncio
async def test_find_farmers_with_limit_exceeding(farmer_controller, mock_request):
    limit = 101
    page = 1
    query = "John"

    with pytest.raises(BadRequestError, match="Limit can be at most 100"):
        await farmer_controller.find_farmers_paginated_and_with_query(mock_request, limit, page, query)

@pytest.mark.asyncio
async def test_delete_farmer_by_id(farmer_controller, mock_farmer_adapter, mock_request):
    farmer_id = 1

    result = await farmer_controller.delete_farmer_by_id(mock_request, farmer_id)

    assert result == {"message": "Farmer deleted"}
    mock_farmer_adapter.delete_farmer_by_id.assert_called_once_with(farmer_id, "trace-12345")
