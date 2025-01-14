import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from ports.outbound.database.models import Farm, Crop, Culture
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort

@pytest.mark.asyncio
class TestOutboundFarmRepositoryPort:
    @pytest.fixture
    def mock_session(self):
        session = MagicMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.refresh = AsyncMock()
        session.add = AsyncMock()
        return session

    @pytest.fixture
    def farm_repository(self, mock_session):
        return OutboundFarmRepositoryPort(session=mock_session)

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_find_farm_counts_grouped_by_state_by_farmer_id_success(self, farm_repository, mock_session, trace_id):        
        mock_result = MagicMock()
        mock_mappings = MagicMock()
        
        mock_mappings.all.return_value = [
            {"state": "State A", "farm_count": 3},
            {"state": "State B", "farm_count": 2},
        ]
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        result = await farm_repository.find_farm_counts_grouped_by_state_by_farmer_id(1, trace_id)

        assert len(result) == 2
        assert result[0]["state"] == "State A"
        assert result[0]["farm_count"] == 3
        assert result[1]["state"] == "State B"
        assert result[1]["farm_count"] == 2

    async def test_find_average_land_use_by_farmer_id_success(self, farm_repository, mock_session, trace_id):
        mock_result = MagicMock()
        one = MagicMock()
        mock_result.one = one
        mock_one_result = MagicMock()
        mock_one_result.average_arable_area = 100.0
        mock_one_result.average_vegetation_area = 50.0
        one.return_value = mock_one_result
        mock_session.execute.return_value = mock_result

        result = await farm_repository.find_average_land_use_by_farmer_id(1, trace_id)

        assert result["average_arable_area"] == 100.0
        assert result["average_vegetation_area"] == 50.0

    async def test_find_farms_ordered_by_vegetation_area_desc_success(self, farm_repository, mock_session, trace_id):
        farm = Farm(id=1, name="Sunny Farm", arable_area=100.5, vegetation_area=50.0, total_area=150.5, farmer_id=1)

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [farm]
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        result = await farm_repository.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(1, trace_id)

        assert len(result) == 1
        assert result[0].id == farm.id

    async def test_find_farm_by_id_success(self, farm_repository, mock_session, trace_id):
        farm = Farm(id=1, name="Sunny Farm", arable_area=100.5, vegetation_area=50.0, total_area=150.5, farmer_id=1)

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = farm
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        result = await farm_repository.find_farm_by_id(1, trace_id)

        assert result.id == farm.id
        assert result.name == farm.name
