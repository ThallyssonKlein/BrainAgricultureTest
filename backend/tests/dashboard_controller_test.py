import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request

from ports.inbound.http.controllers.dashboard_controller import DashboardController

@pytest.fixture
def mock_dashboard_adapter():
    return AsyncMock()


@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.state.trace_id = "trace-12345"
    return request


@pytest.fixture
def dashboard_controller(mock_dashboard_adapter):
    return DashboardController(dashboard_adapter=mock_dashboard_adapter)


@pytest.mark.asyncio
async def test_get_dashboard_data(dashboard_controller, mock_dashboard_adapter, mock_request):
    farmer_id = 1
    dashboard_data = {
        "total_farms": 5,
        "total_area": 150.0,
        "average_arable_area": 30.0,
        "average_vegetation_area": 20.0,
    }

    mock_dashboard_adapter.get_dashboard_data.return_value = dashboard_data

    result = await dashboard_controller.get_dashboard_data(mock_request, farmer_id=farmer_id)

    assert result == dashboard_data
    mock_dashboard_adapter.get_dashboard_data.assert_called_once_with(farmer_id, "trace-12345")
