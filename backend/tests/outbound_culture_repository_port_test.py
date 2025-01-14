import logging
import tracemalloc
import pytest
pytestmark = pytest.mark.asyncio
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import delete, insert, select, update
from ports.outbound.database.models import Culture
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort

tracemalloc.start()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_logger")

@pytest.mark.asyncio
class TestOutboundCultureRepositoryPort:
    @pytest.fixture
    def mock_session(self):
        session = MagicMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        return session

    @pytest.fixture
    def culture_repository(self, mock_session):
        return OutboundCultureRepositoryPort(session=mock_session)

    @pytest.fixture
    def valid_culture_data(self):  # Fixture adicionada
        return {"name": "Wheat"}

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

        # Configuração do mock para scalars e retorno de first
        print("Configurando mocks para scalars e first().")
        # mock_scalars = MagicMock()
        # mock_scalars.first.return_value = created_culture
        # mock_session.execute.return_value.scalars = mock_scalars
        scalars = MagicMock()
        first = MagicMock()
        first.return_value = created_culture
        scalars.return_value.first = first
        mock_session.execute.return_value.scalars = scalars

        # Chamando o método
        print("Chamando método 'create_culture_for_a_farmer'.")
        result = await culture_repository.create_culture_for_a_farmer(farmer_id, valid_culture_data, trace_id)

        # Validar a query executada
        print("Validando a query executada.")
        executed_query = mock_session.execute.call_args[0][0]
        expected_query = (
            insert(Culture)
            .values(name=valid_culture_data["name"], farmer_id=farmer_id)
            .returning(Culture)
        )
        print(f"Query executada: {executed_query}")
        print(f"Query esperada: {expected_query}")
        assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"

        # Validar o resultado
        print("Validando o resultado.")
        assert result == created_culture
        mock_session.commit.assert_called_once()

        print("Fim do teste.")

    async def test_get_cultures_for_a_farmer_query_validation(self, culture_repository, mock_session, trace_id):
        print("Início do teste 'test_get_cultures_for_a_farmer_query_validation'")

        farmer_id = 1
        cultures = [Culture(id=1, name="Wheat", farmer_id=farmer_id)]

        # Adicionando log para o mock dos scalars e do retorno
        print(f"Mockando retorno para cultures: {cultures}")
        scalars = MagicMock()
        all = MagicMock()
        all.return_value = cultures
        scalars.return_value.all = all
        mock_session.execute.return_value.scalars = scalars

        # Adicionando log antes de chamar o método
        print(f"Chamando 'get_cultures_for_a_farmer' com farmer_id={farmer_id} e trace_id={trace_id}")
        result = await culture_repository.get_cultures_for_a_farmer(farmer_id, trace_id)

        # Logs para verificar a query executada
        executed_query = mock_session.execute.call_args[0][0]
        print(f"Query executada: {executed_query}")

        expected_query = select(Culture).where(Culture.farmer_id == farmer_id)
        print(f"Query esperada: {expected_query}")

        # Validações com logs em caso de falha
        try:
            assert str(executed_query) == str(expected_query), f"Query mismatch. Got: {executed_query}"
        except AssertionError as e:
            print(f"Query mismatch! Executed: {executed_query}, Expected: {expected_query}")
            raise e

        try:
            assert result == cultures
        except AssertionError as e:
            print(f"Resultado incorreto! Result: {result}, Expected: {cultures}")
            raise e

        # Log de finalização bem-sucedida
        print(f"Fim do teste. Resultado: {result}")

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
        first = MagicMock()
        first.return_value = updated_culture
        mock_scalars.return_value.first = first
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
