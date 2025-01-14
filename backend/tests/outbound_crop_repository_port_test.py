import pytest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import delete, insert, select, update
from ports.outbound.database.models import Crop, Culture, Farm
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort
from sqlalchemy.orm import selectinload

@pytest.mark.asyncio
class TestOutboundCropRepositoryPort:
    @pytest.fixture
    def mock_session(self):
        session = MagicMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()

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

    async def test_find_crops_by_culture_name_and_farmer_id_query_validation(self, crop_repository, mock_session, trace_id):
        culture_name = "Wheat"
        farmer_id = 1
        crop = Crop(id=1, date="2025-01-01", farm_id=1, culture_id=1)

        scalars = MagicMock()
        all = MagicMock()
        all.return_value = [crop]
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        result = await crop_repository.find_crops_by_culture_name_and_farmer_id(culture_name, farmer_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            select(Crop)
            .join(Crop.farm)
            .join(Crop.culture)
            .where(Culture.name == culture_name)
            .where(Farm.farmer_id == farmer_id)
            .options(
                selectinload(Crop.culture)
            )
        )
        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"

        assert len(result) == 1
        assert result[0].id == crop.id
        mock_session.execute.assert_called_once()
    
    async def test_find_crops_by_culture_name_and_farmer_id_failed_should_call_rollback(self, crop_repository, mock_session, trace_id):
        culture_name = "Wheat"
        farmer_id = 1

        mock_session.execute.side_effect = Exception("Error")
        mock_session.rollback = AsyncMock()

        with pytest.raises(Exception):
            await crop_repository.find_crops_by_culture_name_and_farmer_id(culture_name, farmer_id, trace_id)

        mock_session.execute.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()

    async def test_create_crop_for_a_farm_and_return_with_culture_query_validation(self, crop_repository, mock_session, valid_crop_data, trace_id):
        farm_id = 1
        crop_id = 1
        crop = Crop(id=crop_id, date=valid_crop_data["date"], farm_id=farm_id, culture_id=valid_crop_data["culture"]["id"])

        scalar = MagicMock()
        scalar.return_value = crop_id
        mock_session.execute.return_value.scalar = scalar

        mock_scalars = MagicMock()
        first = MagicMock()
        first.return_value = crop
        mock_scalars.return_value.first = first
        mock_session.execute.return_value.scalars = mock_scalars

        result = await crop_repository.create_crop_for_a_farm_and_return_with_culture(farm_id, valid_crop_data, trace_id)

        executed_insert_query = mock_session.execute.call_args_list[0][0][0]
        expected_insert_query = (
            insert(Crop)
            .values(
                date=valid_crop_data["date"],
                farm_id=farm_id,
                culture_id=valid_crop_data["culture"]["id"],
            )
            .returning(Crop.id)
        )
        assert str(executed_insert_query) == str(expected_insert_query), f"Insert query mismatch. Got: {executed_insert_query}"

        executed_select_query = mock_session.execute.call_args_list[1][0][0]
        expected_select_query = (
            select(Crop)
            .where(Crop.id == crop_id)
            .options(
                selectinload(Crop.culture),
            )
        )
        assert str(executed_select_query) == str(expected_select_query), f"Select query mismatch. Got: {executed_select_query}"

        assert result == crop
        mock_session.execute.assert_called()
        mock_session.commit.assert_called_once()

    async def test_create_crop_for_a_farm_and_return_with_culture_failed_should_call_rollback(
        self, crop_repository, mock_session, valid_crop_data, trace_id
    ):
        print("Início do teste 'test_create_crop_for_a_farm_and_return_with_culture_failed_should_call_rollback'")

        farm_id = 1

        # Configurando o mock para simular exceção
        mock_session.execute = AsyncMock(side_effect=Exception("Error"))
        mock_session.rollback = AsyncMock()

        # Validando que a exceção é levantada
        with pytest.raises(Exception) as exc_info:
            await crop_repository.create_crop_for_a_farm_and_return_with_culture(farm_id, valid_crop_data, trace_id)

        print(f"Exceção capturada: {exc_info.value}")

        # Verificações sobre o comportamento do mock
        mock_session.execute.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()

        print("Fim do teste 'test_create_crop_for_a_farm_and_return_with_culture_failed_should_call_rollback'")
    
    async def test_update_crop_by_id_query_validation(self, crop_repository, mock_session, valid_crop_data, trace_id):
        crop_id = 1
        updated_crop = Crop(id=crop_id, date=valid_crop_data["date"], farm_id=1, culture_id=1)

        scalars = MagicMock()
        first = MagicMock()
        scalars.return_value.first = first
        first.return_value = updated_crop
        mock_session.execute.return_value.scalars = scalars

        result = await crop_repository.update_crop_by_id(crop_id, valid_crop_data, trace_id)

        executed_update_query = mock_session.execute.call_args_list[0][0][0]
        expected_update_query = (
            update(Crop)
            .where(Crop.id == crop_id)
            .values(
                date=valid_crop_data["date"],
                culture_id=valid_crop_data["culture"]["id"],
            )
            .execution_options(synchronize_session="fetch")
        )
        assert str(executed_update_query) == str(expected_update_query), f"Update query mismatch. Got: {executed_update_query}"

        executed_select_query = mock_session.execute.call_args_list[1][0][0]
        expected_select_query = (
            select(Crop)
            .where(Crop.id == crop_id)
            .options(
                selectinload(Crop.culture),
                selectinload(Crop.farm),
            )
        )
        assert str(executed_select_query) == str(expected_select_query), f"Select query mismatch. Got: {executed_select_query}"

        assert result == updated_crop
        mock_session.execute.assert_called()
        mock_session.commit.assert_called_once()
    
    async def test_update_crop_by_id_failed_should_call_rollback(self, crop_repository, mock_session, valid_crop_data, trace_id):
        crop_id = 1

        mock_session.execute.side_effect = Exception("Error")

        with pytest.raises(Exception):
            await crop_repository.update_crop_by_id(crop_id, valid_crop_data, trace_id)

        mock_session.execute.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()

    async def test_delete_crop_by_id_query_validation(self, crop_repository, mock_session, trace_id):
        crop_id = 1

        mock_result = MagicMock()
        mock_session.execute.return_value = mock_result

        result = await crop_repository.delete_crop_by_id(crop_id, trace_id)

        executed_query = mock_session.execute.call_args[0][0]

        expected_query = delete(Crop).where(Crop.id == crop_id)
        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"

        assert result == mock_result
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    
    async def test_delete_crop_by_id_success_failed_should_call_rollback(self, crop_repository, mock_session, trace_id):
        crop_id = 1

        mock_session.execute.side_effect = Exception("Error")
        mock_session.rollback = AsyncMock()

        with pytest.raises(Exception):
            await crop_repository.delete_crop_by_id(crop_id, trace_id)

        mock_session.execute.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.commit.assert_not_called()
