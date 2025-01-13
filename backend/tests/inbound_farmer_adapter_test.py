import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.person.invalid_cpf_error import InvalidCPFError
from domain.person.invalid_cnpj_error import InvalidCNPJError
from ports.inbound.http.error.bad_request_error import BadRequestError
from ports.inbound.http.error.conflict_error import ConflictError
from ports.inbound.http.error.not_found_error import NotFoundError
from sqlalchemy.exc import IntegrityError
from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter
from pydantic import BaseModel

class MockFarmerSchema(BaseModel):
    name: str
    document: str

    def model_dump(self, *args, **kwargs):
        return super().model_dump(*args, **kwargs)


@pytest.mark.asyncio
class TestInboundFarmerAdapter:
    @pytest.fixture
    def mock_adapters(self):
        return {
            "outbound_farmer_repository_port": AsyncMock(),
            "person_service": MagicMock(),
            "outbound_culture_repository_port": AsyncMock(),
            "outbound_crop_repository_port": AsyncMock(),
            "outbound_farm_repository_port": AsyncMock(),
        }

    @pytest.fixture
    def farmer_adapter(self, mock_adapters):
        return InboundFarmerAdapter(
            outbound_farmer_repository_port=mock_adapters["outbound_farmer_repository_port"],
            person_service=mock_adapters["person_service"],
            outbound_culture_repository_port=mock_adapters["outbound_culture_repository_port"],
            outbound_crop_repository_port=mock_adapters["outbound_crop_repository_port"],
            outbound_farm_repository_port=mock_adapters["outbound_farm_repository_port"],
        )

    @pytest.fixture
    def valid_farmer(self):
        return MockFarmerSchema(name="John Doe", document="12345678901")

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_farmer_success_with_cpf(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        mock_adapters["outbound_farmer_repository_port"].create_farmer.return_value = {
            "id": 1,
            "name": "John Doe",
            "document": "12345678901",
        }

        result = await farmer_adapter.create_farmer(valid_farmer, trace_id)

        assert result["name"] == "John Doe"
        assert result["document"] == "12345678901"

        mock_adapters["person_service"].validate_cpf.assert_called_once_with("12345678901")
        mock_adapters["outbound_farmer_repository_port"].create_farmer.assert_called_once_with(
            valid_farmer.model_dump(), trace_id
        )
    
    async def test_create_farmer_success_with_cnpj(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        valid_farmer.document = "12345678901234"
        mock_adapters["outbound_farmer_repository_port"].create_farmer.return_value = {
            "id": 1,
            "name": "John Doe",
            "document": "12345678901234",
        }

        result = await farmer_adapter.create_farmer(valid_farmer, trace_id)

        assert result["name"] == "John Doe"
        assert result["document"] == "12345678901234"

        mock_adapters["person_service"].validate_cnpj.assert_called_once_with("12345678901234")
        mock_adapters["outbound_farmer_repository_port"].create_farmer.assert_called_once_with(
            valid_farmer.model_dump(), trace_id
        )

    async def test_create_farmer_invalid_cpf(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        mock_adapters["person_service"].validate_cpf.side_effect = InvalidCPFError("Invalid CPF")

        with pytest.raises(BadRequestError, match="Invalid CPF"):
            await farmer_adapter.create_farmer(valid_farmer, trace_id)
    
    async def test_create_fermer_invalid_cnpj(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        mock_adapters["person_service"].validate_cpf.side_effect = InvalidCNPJError("Invalid CNPJ")

        with pytest.raises(BadRequestError, match="Invalid CNPJ"):
            await farmer_adapter.create_farmer(valid_farmer, trace_id)

    async def test_create_farmer_conflict(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        mock_adapters["outbound_farmer_repository_port"].create_farmer.side_effect = IntegrityError(
            statement="INSERT INTO farmers",
            params=None,
            orig=Exception("duplicate key value violates unique constraint"),
        )

        with pytest.raises(ConflictError, match="Farmer already exists"):
            await farmer_adapter.create_farmer(valid_farmer, trace_id)

    async def test_update_farmer_success(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        mock_adapters["outbound_farmer_repository_port"].update_farmer.return_value = {
            "id": 1,
            "name": "John Doe Updated",
            "document": "12345678901",
        }

        result = await farmer_adapter.update_farmer(1, valid_farmer, trace_id)

        assert result["name"] == "John Doe Updated"

        mock_adapters["person_service"].validate_cpf.assert_called_once_with("12345678901")
        mock_adapters["outbound_farmer_repository_port"].update_farmer.assert_called_once_with(
            {"id": 1, **valid_farmer.model_dump()}, trace_id
        )

    async def test_update_farmer_not_found(self, farmer_adapter, mock_adapters, valid_farmer, trace_id):
        mock_adapters["outbound_farmer_repository_port"].update_farmer.side_effect = ValueError("Farmer not found")

        with pytest.raises(NotFoundError, match="Farmer not found"):
            await farmer_adapter.update_farmer(1, valid_farmer, trace_id)

    async def test_find_farmers_paginated_success(self, farmer_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_farmer_repository_port"].find_farmers_paginated_and_with_query.return_value = [
            {"id": 1, "name": "John Doe", "document": "12345678901"},
            {"id": 2, "name": "Jane Doe", "document": "98765432100"},
        ]

        result = await farmer_adapter.find_farmers_paginated_and_with_query(10, 0, "Doe", trace_id)

        assert len(result) == 2
        assert result[0]["name"] == "John Doe"

        mock_adapters["outbound_farmer_repository_port"].find_farmers_paginated_and_with_query.assert_called_once_with(
            10, 0, "Doe", trace_id
        )

    async def test_delete_farmer_success(self, farmer_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_farmer_repository_port"].delete_farmer_by_id.return_value = MagicMock(rowcount=1)

        await farmer_adapter.delete_farmer_by_id(1, trace_id)

        mock_adapters["outbound_farmer_repository_port"].delete_farmer_by_id.assert_called_once_with(1, trace_id)

    async def test_delete_farmer_not_found(self, farmer_adapter, mock_adapters, trace_id):
        mock_adapters["outbound_farmer_repository_port"].delete_farmer_by_id.return_value = MagicMock(rowcount=0)

        with pytest.raises(NotFoundError, match="Farmer not found"):
            await farmer_adapter.delete_farmer_by_id(1, trace_id)
