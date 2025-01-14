import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy import delete, insert, select, func, update
from ports.outbound.database.models import Culture, Farm, Crop
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from sqlalchemy.orm import selectinload

class TotalFarmsAndHectares:
    def __init__(self, farm_count, total_hectares):
        self.farm_count = farm_count
        self.total_hectares = total_hectares

class AverageLandUse:
    def __init__(self, average_arable_area, average_vegetation_area):
        self.average_arable_area = average_arable_area
        self.average_vegetation_area = average_vegetation_area

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

    @pytest.fixture
    def valid_farm_data(self):
        return {
            "name": "Farm A",
            "arable_area": 50,
            "vegetation_area": 20,
            "total_area": 70,
            "city": "City A",
            "state": "State A"
        }

    async def test_find_farm_counts_grouped_by_state_by_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        
        mappings = MagicMock()
        all = MagicMock()
        all.return_value = [{"state": "State A", "farm_count": 2}]
        mappings.return_value.all = all
        mock_session.execute.return_value.mappings = mappings

        result = await farm_repository.find_farm_counts_grouped_by_state_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(
            Farm.state.label("state"),
            func.count(Farm.id).label("farm_count")
        ).where(Farm.farmer_id == farmer_id).group_by(Farm.state)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == [{"state": "State A", "farm_count": 2}]

    async def test_find_farms_ordered_by_vegetation_area_desc_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        farms = [Farm(id=1, name="Farm A", vegetation_area=20, farmer_id=farmer_id)]
        
        scalars = MagicMock()
        all = MagicMock()
        all.return_value = farms
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        result = await farm_repository.find_farms_ordered_by_vegetation_area_desc_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(Farm).where(Farm.farmer_id == farmer_id).order_by(Farm.vegetation_area.desc()).options(
            selectinload(Farm.crops).selectinload(Crop.culture)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == farms

    async def test_find_farm_by_id_query_validation(self, farm_repository, mock_session, trace_id):
        farm_id = 1
        farm = Farm(id=farm_id, name="Farm A", farmer_id=1)
        
        scalars = MagicMock()
        first = MagicMock()
        first.return_value = farm
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        result = await farm_repository.find_farm_by_id(farm_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(Farm).where(Farm.id == farm_id)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == farm
    
    
    async def test_find_farms_ordered_by_arable_area_desc_by_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        farms = [Farm(id=1, name="Farm A", farmer_id=farmer_id)]

        scalars = MagicMock()
        all = MagicMock()
        all.return_value = farms
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        result = await farm_repository.find_farms_ordered_by_arable_area_desc_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(Farm)
            .where(Farm.farmer_id == farmer_id)
            .order_by(Farm.arable_area.desc())
            .options(selectinload(Farm.crops).selectinload(Crop.culture))
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == farms

    async def test_create_farm_for_a_farmer_query_validation(self, farm_repository, mock_session, valid_farm_data, trace_id):
        farmer_id = 1
        created_farm = Farm(
            id=1,
            name=valid_farm_data["name"],
            arable_area=valid_farm_data["arable_area"],
            vegetation_area=valid_farm_data["vegetation_area"],
            total_area=valid_farm_data["vegetation_area"] + valid_farm_data["arable_area"],
            farmer_id=farmer_id,
            city=valid_farm_data["city"],
            state=valid_farm_data["state"],
        )

        scalars = MagicMock()
        first = MagicMock()
        first.return_value = created_farm
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        result = await farm_repository.create_farm_for_a_farmer(farmer_id, valid_farm_data, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            insert(Farm)
            .values(
                name=valid_farm_data["name"],
                arable_area=valid_farm_data["arable_area"],
                vegetation_area=valid_farm_data["vegetation_area"],
                total_area=valid_farm_data["vegetation_area"] + valid_farm_data["arable_area"],
                farmer_id=farmer_id,
                city=valid_farm_data["city"],
                state=valid_farm_data["state"],
            )
            .returning(Farm)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == created_farm
        mock_session.commit.assert_called_once()

    async def test_update_farm_by_id_query_validation(self, farm_repository, mock_session, valid_farm_data, trace_id):
        farm_id = 1
        updated_farm = Farm(
            id=farm_id,
            name=valid_farm_data["name"],
            arable_area=valid_farm_data["arable_area"],
            vegetation_area=valid_farm_data["vegetation_area"],
            total_area=valid_farm_data["vegetation_area"] + valid_farm_data["arable_area"],
            city=valid_farm_data["city"],
            state=valid_farm_data["state"],
        )

        scalars = MagicMock()
        first = MagicMock()
        first.return_value = updated_farm
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        result = await farm_repository.update_farm_by_id(farm_id, valid_farm_data, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            update(Farm)
            .where(Farm.id == farm_id)
            .values(
                name=valid_farm_data["name"],
                arable_area=valid_farm_data["arable_area"],
                vegetation_area=valid_farm_data["vegetation_area"],
                total_area=valid_farm_data["vegetation_area"] + valid_farm_data["arable_area"],
                city=valid_farm_data["city"],
                state=valid_farm_data["state"],
            )
            .returning(Farm)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == updated_farm
        mock_session.commit.assert_called_once()

    async def test_delete_farm_by_id_query_validation(self, farm_repository, mock_session, trace_id):
        farm_id = 1

        mock_session.execute.return_value = AsyncMock()

        result = await farm_repository.delete_farm_by_id(farm_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = delete(Farm).where(Farm.id == farm_id)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == mock_session.execute.return_value
        mock_session.commit.assert_called_once()
    
    async def test_find_farm_counts_grouped_by_state_by_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        mock_result = [{"state": "IL", "farm_count": 3}]

        mappings = MagicMock()
        all = MagicMock()
        all.return_value = mock_result
        mappings.return_value.all = all
        mock_session.execute.return_value.mappings = mappings

        result = await farm_repository.find_farm_counts_grouped_by_state_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(
                Farm.state.label("state"),
                func.count(Farm.id).label("farm_count")
            ).where(Farm.farmer_id == farmer_id).group_by(Farm.state)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == mock_result

    async def test_find_farms_count_grouped_by_culture_by_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        mock_result = [{"culture": "Wheat", "farm_count": 2}]

        mappings = MagicMock()
        all = MagicMock()
        all.return_value = mock_result
        mappings.return_value.all = all
        mock_session.execute.return_value.mappings = mappings

        result = await farm_repository.find_farms_count_grouped_by_culture_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(
                Culture.name.label("culture"),
                func.count(Farm.id).label("farm_count")
            )
            .join(Crop, Crop.farm_id == Farm.id)
            .join(Culture, Culture.id == Crop.culture_id)
            .where(Farm.farmer_id == farmer_id)
            .group_by(Culture.name)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == mock_result

    async def test_find_average_land_use_by_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        mock_result = AverageLandUse(average_arable_area=10, average_vegetation_area=5)

        one = MagicMock()
        one.return_value = mock_result
        mock_session.execute.return_value.one = one        

        result = await farm_repository.find_average_land_use_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(
                func.coalesce(func.avg(Farm.arable_area), 0).label("average_arable_area"),
                func.coalesce(func.avg(Farm.vegetation_area), 0).label("average_vegetation_area")
            ).where(Farm.farmer_id == farmer_id)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result['average_arable_area'] == 10
        assert result['average_vegetation_area'] == 5

    async def test_find_total_farms_and_hectares_by_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        mock_result = TotalFarmsAndHectares(farm_count=3, total_hectares=50)

        one = MagicMock()
        one.return_value = mock_result
        mock_session.execute.return_value.one = one

        result = await farm_repository.find_total_farms_and_hectares_by_farmer_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(
                func.count(Farm.id).label("farm_count"),
                func.coalesce(func.sum(Farm.total_area), 0).label("total_hectares")
            ).where(Farm.farmer_id == farmer_id)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result["farm_count"] == 3
        assert result["total_hectares"] == 50

    async def test_find_farms_by_state_and_farmer_id_query_validation(self, farm_repository, mock_session, trace_id):
        farmer_id = 1
        state = "IL"
        farms = [Farm(id=1, name="Farm A", farmer_id=farmer_id, state=state)]

        scalars = MagicMock()
        all = MagicMock()
        all.return_value = farms
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        result = await farm_repository.find_farms_by_state_and_farmer_id(farmer_id, state, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(Farm)
            .where(Farm.farmer_id == farmer_id, Farm.state == state)
            .options(selectinload(Farm.crops).selectinload(Crop.culture))
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == farms
