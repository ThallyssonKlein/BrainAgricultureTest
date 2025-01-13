import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from ports.outbound.database.models import Farmer
from ports.outbound.database.outbound_farmer_repository_port import OutboundFarmerRepositoryPort

@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def farmer_repository(mock_session):
    return OutboundFarmerRepositoryPort(session=mock_session)


@pytest.fixture
def trace_id():
    return "trace-12345"


@pytest.mark.asyncio
async def test_create_farmer_success(farmer_repository, mock_session, trace_id):
    farmer_data = {
        "document": "123456789",
        "name": "John Doe",
        "city": "Smalltown",
        "state": "ST",
    }
    mock_result = MagicMock()
    farmer = Farmer(**farmer_data, id=1)
    mock_result.scalars.return_value.first.return_value = farmer
    mock_session.execute.return_value = mock_result

    result = await farmer_repository.create_farmer(farmer_data, trace_id)

    assert result.id == 1
    assert result.document == farmer_data["document"]
    assert result.name == farmer_data["name"]
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_farmer_integrity_error(farmer_repository, mock_session, trace_id):
    farmer_data = {
        "document": "123456789",
        "name": "John Doe",
        "city": "Smalltown",
        "state": "ST",
    }
    mock_session.execute.side_effect = IntegrityError("duplicate key", {}, None)

    with pytest.raises(ValueError, match="Farmer with this document already exists"):
        await farmer_repository.create_farmer(farmer_data, trace_id)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_update_farmer_success(farmer_repository, mock_session, trace_id):
    farmer_data = {
        "id": 1,
        "document": "987654321",
        "name": "John Updated",
        "city": "Updatedtown",
        "state": "UT",
    }
    mock_result = MagicMock()
    farmer = Farmer(**farmer_data)
    mock_result.scalars.return_value.first.return_value = farmer
    mock_session.execute.return_value = mock_result

    result = await farmer_repository.update_farmer(farmer_data, trace_id)

    assert result.id == farmer_data["id"]
    assert result.document == farmer_data["document"]
    assert result.name == farmer_data["name"]
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_farmer_not_found(farmer_repository, mock_session, trace_id):
    farmer_data = {
        "id": 1,
        "document": "987654321",
        "name": "John Updated",
        "city": "Updatedtown",
        "state": "UT",
    }
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result

    with pytest.raises(ValueError, match="Farmer not found"):
        await farmer_repository.update_farmer(farmer_data, trace_id)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_find_farmers_paginated_and_with_query_success(farmer_repository, mock_session, trace_id):
    farmer = Farmer(id=1, document="123456789", name="John Doe", city="Smalltown", state="ST")
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [farmer]
    mock_session.execute.return_value = mock_result

    result = await farmer_repository.find_farmers_paginated_and_with_query(10, 0, "John", trace_id)

    assert len(result) == 1
    assert result[0].name == "John Doe"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_delete_farmer_by_id_success(farmer_repository, mock_session, trace_id):
    mock_result = MagicMock(rowcount=1)
    mock_session.execute.return_value = mock_result

    result = await farmer_repository.delete_farmer_by_id(1, trace_id)

    assert result.rowcount == 1
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_find_farmer_by_id_success(farmer_repository, mock_session, trace_id):
    farmer = Farmer(id=1, document="123456789", name="John Doe", city="Smalltown", state="ST")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = farmer
    mock_session.execute.return_value = mock_result

    result = await farmer_repository.find_farmer_by_id(1, trace_id)

    assert result.id == 1
    assert result.name == "John Doe"
    mock_session.execute.assert_called_once()
