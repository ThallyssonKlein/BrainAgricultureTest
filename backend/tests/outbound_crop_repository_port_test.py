import pytest
from unittest.mock import AsyncMock, MagicMock
from ports.outbound.database.models import Crop
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort

@pytest.mark.asyncio
class TestOutboundCropRepositoryPort:
    @pytest.fixture
    def mock_session(self):
        session = AsyncMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.refresh = AsyncMock()
        session.add = AsyncMock()
        return session

    @pytest.fixture
    def crop_repository(self, mock_session):
        return OutboundCropRepositoryPort(session=mock_session)

    @pytest.fixture
    def valid_crop_data(self):
        return {
            "date": "2025-01-01",
            "culture": {"id": 1},
        }

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_find_crops_by_culture_name_and_farmer_id_success(self, crop_repository, mock_session, trace_id):
        crop = Crop(id=1, date="2025-01-01", farm_id=1, culture_id=1)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [crop]
        mock_session.execute.return_value.scalars = MagicMock(return_value=mock_scalars)

        result = await crop_repository.find_crops_by_culture_name_and_farmer_id("Wheat", 1, trace_id)

        assert len(result) == 1
        assert result[0].id == crop.id

        mock_session.execute.assert_called_once()
