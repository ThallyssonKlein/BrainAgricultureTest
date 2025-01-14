import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy import insert, update, delete, select
from sqlalchemy.exc import IntegrityError
from ports.outbound.database.models import Farmer
from ports.outbound.database.outbound_farmer_repository_port import OutboundFarmerRepositoryPort

@pytest.mark.asyncio
class TestOutboundFarmerRepositoryPort:
    @pytest.fixture
    def mock_session(self):
        session = AsyncMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        return session

    @pytest.fixture
    def farmer_repository(self, mock_session):
        return OutboundFarmerRepositoryPort(session=mock_session)

    @pytest.fixture
    def trace_id(self):
        return "trace-12345"

    async def test_create_farmer_query_validation(self, farmer_repository, mock_session, trace_id):
        farmer_data = {
            "document": "12345678901",
            "name": "John Doe",
            "city": "Springfield",
            "state": "IL",
        }
        created_farmer = Farmer(**farmer_data)

        scalars = MagicMock()
        first = MagicMock()
        first.return_value = created_farmer
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        result = await farmer_repository.create_farmer(farmer_data, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            insert(Farmer)
            .values(
                document=farmer_data["document"],
                name=farmer_data["name"],
                city=farmer_data["city"],
                state=farmer_data["state"],
            )
            .returning(Farmer)
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == created_farmer
        mock_session.commit.assert_called_once()

    async def test_update_farmer_query_validation(self, farmer_repository, mock_session, trace_id):
        farmer_data = {
            "id": 1,
            "document": "12345678901",
            "name": "John Doe Updated",
            "city": "Springfield",
            "state": "IL",
        }
        updated_farmer = Farmer(**farmer_data)

        scalars = MagicMock()
        first = MagicMock()
        first.return_value = updated_farmer
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        result = await farmer_repository.update_farmer(farmer_data, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            update(Farmer)
            .where(Farmer.id == farmer_data["id"])
            .values(
                document=farmer_data["document"],
                name=farmer_data["name"],
                city=farmer_data["city"],
                state=farmer_data["state"],
            )
            .returning(Farmer)
            .execution_options(synchronize_session="fetch")
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == updated_farmer
        mock_session.commit.assert_called_once()

    async def test_find_farmers_paginated_and_with_query_validation(self, farmer_repository, mock_session, trace_id):
        farmers = [Farmer(id=1, name="John Doe", city="Springfield", state="IL")]
        
        scalars = MagicMock()
        all = MagicMock()
        all.return_value = farmers
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        limit = 10
        offset = 1
        query = "John"
        result = await farmer_repository.find_farmers_paginated_and_with_query(limit, offset, query, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(Farmer)
            .offset(offset - 1)
            .limit(limit)
            .where(Farmer.name.ilike(f"%{query}%"))
        )

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == farmers

    async def test_delete_farmer_by_id_query_validation(self, farmer_repository, mock_session, trace_id):
        farmer_id = 1

        mock_session.execute.return_value = AsyncMock()

        await farmer_repository.delete_farmer_by_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = delete(Farmer).where(Farmer.id == farmer_id)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        mock_session.commit.assert_called_once()

    async def test_find_farmer_by_id_query_validation(self, farmer_repository, mock_session, trace_id):
        farmer_id = 1
        farmer = Farmer(id=farmer_id, name="John Doe", city="Springfield", state="IL")

        scalars = MagicMock()
        first = MagicMock()
        first.return_value = farmer
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        result = await farmer_repository.find_farmer_by_id(farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = select(Farmer).where(Farmer.id == farmer_id)

        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        assert result == farmer
    
    async def test_create_farmer_integrity_error(self, farmer_repository, mock_session, trace_id):
        farmer_data = {
            "document": "12345678901",
            "name": "John Doe",
            "city": "Springfield",
            "state": "IL",
        }

        mock_session.execute.side_effect = IntegrityError("IntegrityError", {}, None)

        with pytest.raises(ValueError, match="Farmer with this document already exists"):
            await farmer_repository.create_farmer(farmer_data, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()

    async def test_update_farmer_not_found(self, farmer_repository, mock_session, trace_id):
        farmer_data = {
            "id": 1,
            "document": "12345678901",
            "name": "John Doe Updated",
            "city": "Springfield",
            "state": "IL",
        }

        scalars = MagicMock()
        first = MagicMock()
        first.return_value = None
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        with pytest.raises(ValueError, match="Farmer not found"):
            await farmer_repository.update_farmer(farmer_data, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_called_once()

    async def test_find_farmer_by_id_query_validation_failed_should_rollback(self, farmer_repository, mock_session, trace_id):
        farmer_id = 1

        mock_session.execute.side_effect = Exception("Error")

        with pytest.raises(Exception, match="Error"):
            await farmer_repository.find_farmer_by_id(farmer_id, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()
    
    async def test_delete_farmer_by_id_query_validation_faild_should_rollback(self, farmer_repository, mock_session, trace_id):
        farmer_id = 1

        mock_session.execute.side_effect = Exception("Error")

        with pytest.raises(Exception, match="Error"):
            await farmer_repository.delete_farmer_by_id(farmer_id, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()
    
    async def test_find_farmers_paginated_and_with_query_validation_failed_should_rollback(self, farmer_repository, mock_session, trace_id):
        limit = 10
        offset = 1
        query = "John"

        mock_session.execute.side_effect = Exception("Error")

        with pytest.raises(Exception, match="Error"):
            await farmer_repository.find_farmers_paginated_and_with_query(limit, offset, query, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()
    
    async def test_update_farmer_query_validation_failed_should_rollback(self, farmer_repository, mock_session, trace_id):
        farmer_data = {
            "id": 1,
            "document": "12345678901",
            "name": "John Doe Updated",
            "city": "Springfield",
            "state": "IL",
        }

        mock_session.execute.side_effect = Exception("Error")

        with pytest.raises(Exception, match="Error"):
            await farmer_repository.update_farmer(farmer_data, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()
    
    async def test_create_farmer_query_validation_failed_should_rollback(self, farmer_repository, mock_session, trace_id):
        farmer_data = {
            "document": "12345678901",
            "name": "John Doe",
            "city": "Springfield",
            "state": "IL",
        }

        mock_session.execute.side_effect = Exception("Error")

        with pytest.raises(Exception, match="Error"):
            await farmer_repository.create_farmer(farmer_data, trace_id)

        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()