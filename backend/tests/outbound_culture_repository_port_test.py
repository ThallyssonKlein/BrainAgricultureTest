import pytest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import delete, insert, select, update
from ports.outbound.database.models import Culture
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort

@pytest.mark.asyncio
class TestOutboundCultureRepositoryPort:
    @pytest.fixture
    def mock_session(self):
        session = AsyncMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        return session

    @pytest.fixture
    def culture_repository(self, mock_session):
        return OutboundCultureRepositoryPort(session=mock_session)

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_delete_culture_query_validation(self, culture_repository, mock_session, trace_id):
        culture_id = 1

        await culture_repository.delete_culture(culture_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = delete(Culture).where(Culture.id == culture_id)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        mock_session.commit.assert_called_once()

    async def test_create_culture_for_a_farmer_query_validation(self, culture_repository, mock_session, valid_culture_data, trace_id):
        farmer_id = 1
        created_culture = Culture(id=1, name=valid_culture_data["name"], farmer_id=farmer_id)

        mock_scalars = MagicMock()
        mock_scalars.first.return_value = created_culture
        mock_session.execute.return_value.scalars = mock_scalars

        result = await culture_repository.create_culture_for_a_farmer(farmer_id, valid_culture_data, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            insert(Culture)
            .values(name=valid_culture_data["name"], farmer_id=farmer_id)
            .returning(Culture)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == created_culture
        mock_session.commit.assert_called_once()

    async def test_get_cultures_for_a_farmer_query_validation(self, culture_repository, mock_session, trace_id):
        farmer_id = 1
        cultures = [Culture(id=1, name="Wheat", farmer_id=farmer_id)]

        scalars = MagicMock()
        all = MagicMock()
        all.return_value = cultures
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        result = await culture_repository.get_cultures_for_a_farmer(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(Culture).where(Culture.farmer_id == farmer_id)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == cultures

    async def test_get_by_farmer_id_and_name_query_validation(self, culture_repository, mock_session, trace_id):
        farmer_id = 1
        culture_name = "Wheat"
        culture = Culture(id=1, name=culture_name, farmer_id=farmer_id)

        scalar_one_or_none = MagicMock()
        scalar_one_or_none.return_value = culture
        mock_session.execute.return_value.scalar_one_or_none = scalar_one_or_none

        result = await culture_repository.get_by_farmer_id_and_name(farmer_id, culture_name, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(Culture).where(Culture.farmer_id == farmer_id, Culture.name == culture_name).limit(1)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == culture

    async def test_update_culture_by_id_query_validation(self, culture_repository, mock_session, valid_culture_data, trace_id):
        culture_id = 1
        updated_culture = Culture(id=culture_id, name=valid_culture_data["name"], farmer_id=1)

        mock_scalars = MagicMock()
        mock_scalars.first.return_value = updated_culture
        mock_session.execute.return_value.scalars = mock_scalars

        result = await culture_repository.update_culture_by_id(culture_id, valid_culture_data, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            update(Culture)
            .where(Culture.id == culture_id)
            .values(name=valid_culture_data["name"])
            .returning(Culture)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == updated_culture
        mock_session.commit.assert_called_once()

    async def test_find_culture_by_id_query_validation(self, culture_repository, mock_session, trace_id):
        culture_id = 1
        culture = Culture(id=culture_id, name="Wheat", farmer_id=1)

        scalar_one_or_none = MagicMock()
        scalar_one_or_none.return_value = culture
        mock_session.execute.return_value.scalar_one_or_none = scalar_one_or_none

        result = await culture_repository.find_culture_by_id(culture_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(Culture).where(Culture.id == culture_id).limit(1)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == culture
