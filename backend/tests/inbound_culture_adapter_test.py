import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from ports.inbound.http.error.conflict_error import ConflictError
from ports.inbound.http.error.not_found_error import NotFoundError
from adapters.inbound.http.inbound_culture_adapter import InboundCultureAdapter
from pydantic import BaseModel

class MockCultureSchema(BaseModel):
    name: str

    def model_dump(self, *args, **kwargs):
        """Mock do método model_dump do Pydantic para aceitar argumentos opcionais."""
        return super().model_dump(*args, **kwargs)


@pytest.mark.asyncio
class TestInboundCultureAdapter:
    @pytest.fixture
    def mock_adapters(self):
        return {
            "outbound_culture_repository_port": AsyncMock(),
            "culture_service": AsyncMock(),
        }

    @pytest.fixture
    def inbound_culture_adapter(self, mock_adapters):
        return InboundCultureAdapter(
            outbound_culture_repository_port=mock_adapters["outbound_culture_repository_port"],
            culture_service=mock_adapters["culture_service"],
        )

    @pytest.fixture
    def valid_culture(self):
        return MockCultureSchema(name="Cereal")

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_culture_success(self, inbound_culture_adapter, mock_adapters, valid_culture, trace_id):
        mock_adapters["culture_service"].create_culture_for_a_farmer.return_value = {
            "id": 1,
            "name": "Cereal",
        }

        result = await inbound_culture_adapter.create_culture_for_a_farmer(101, valid_culture, trace_id)

        assert result["name"] == "Cereal"

        mock_adapters["culture_service"].create_culture_for_a_farmer.assert_called_once_with(
            101, valid_culture.model_dump(), trace_id
        )

    async def test_create_culture_already_exists(self, inbound_culture_adapter, mock_adapters, valid_culture, trace_id):
        mock_adapters["culture_service"].create_culture_for_a_farmer.side_effect = CultureAlreadyExistsError()

        with pytest.raises(ConflictError, match="Culture already exists"):
            await inbound_culture_adapter.create_culture_for_a_farmer(101, valid_culture, trace_id)

    async def test_get_cultures_success(self, inbound_culture_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_culture_repository_port"].get_cultures_for_a_farmer.return_value = [
            {"id": 1, "name": "Cereal"},
            {"id": 2, "name": "Vegetable"},
        ]

        result = await inbound_culture_adapter.get_cultures_for_a_farmer(101, trace_id)

        assert len(result) == 2
        assert result[0]["name"] == "Cereal"

        mock_adapters["outbound_culture_repository_port"].get_cultures_for_a_farmer.assert_called_once_with(101, trace_id)

    async def test_update_culture_success(self, inbound_culture_adapter, mock_adapters, valid_culture, trace_id):
        mock_adapters["culture_service"].update_culture_by_id.return_value = {"id": 1, "name": "Cereal"}

        result = await inbound_culture_adapter.update_culture_by_id(1, valid_culture, trace_id)

        assert result["name"] == "Cereal"

        mock_adapters["culture_service"].update_culture_by_id.assert_called_once_with(
            1, valid_culture.model_dump(), trace_id
        )

    async def test_update_culture_not_found(self, inbound_culture_adapter, mock_adapters, valid_culture, trace_id):
        mock_adapters["culture_service"].update_culture_by_id.side_effect = ValueError("Culture not found")

        with pytest.raises(NotFoundError, match="Culture not found"):
            await inbound_culture_adapter.update_culture_by_id(1, valid_culture, trace_id)
    
    async def test_update_culture_culture_already_exists(self, inbound_culture_adapter, mock_adapters, valid_culture, trace_id):
        mock_adapters["culture_service"].update_culture_by_id.side_effect = CultureAlreadyExistsError()

        with pytest.raises(ConflictError, match="Culture already exists"):
            await inbound_culture_adapter.update_culture_by_id(1, valid_culture, trace_id)

    async def test_delete_culture_success(self, inbound_culture_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_culture_repository_port"].delete_culture_by_id.return_value = MagicMock(rowcount=1)

        await inbound_culture_adapter.delete_culture_by_id(1, trace_id)

        mock_adapters["outbound_culture_repository_port"].delete_culture_by_id.assert_called_once_with(1, trace_id)

    async def test_delete_culture_not_found(self, inbound_culture_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_culture_repository_port"].delete_culture_by_id.return_value = MagicMock(rowcount=0)

        with pytest.raises(NotFoundError, match="Culture not found"):
            await inbound_culture_adapter.delete_culture_by_id(1, trace_id)

    async def test_delete_culture_in_use(self, inbound_culture_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_culture_repository_port"].delete_culture_by_id.side_effect = Exception(
            "violates foreign key constraint"
        )

        with pytest.raises(ConflictError, match="This culture is being used by a crop"):
            await inbound_culture_adapter.delete_culture_by_id(1, trace_id)
