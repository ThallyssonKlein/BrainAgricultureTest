import pytest
from unittest.mock import AsyncMock, MagicMock
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

    async def test_get_by_farmer_id_and_name_success(self, culture_repository, mock_session, trace_id):
        culture = Culture(id=1, name="Cereal", farmer_id=1)

        mock_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=culture)

        result = await culture_repository.get_by_farmer_id_and_name(1, "Cereal", trace_id)

        assert result.id == culture.id
        assert result.name == culture.name

        mock_session.execute.assert_called_once()

    async def test_find_culture_by_id_success(self, culture_repository, mock_session, trace_id):
        culture = Culture(id=1, name="Cereal", farmer_id=1)

        mock_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=culture)

        result = await culture_repository.find_culture_by_id(1, trace_id)

        assert result.id == culture.id
        assert result.name == culture.name

        mock_session.execute.assert_called_once()
