import pytest
from domain.person.invalid_cpf_error import InvalidCPFError
from domain.person.invalid_cnpj_error import InvalidCNPJError
from domain.person.person_service import PersonService

class TestPersonService:
    @pytest.fixture
    def person_service(self):
        return PersonService()

    def test_validate_cpf_valid(self, person_service):
        valid_cpf = "123.456.789-09"
        assert person_service.validate_cpf(valid_cpf) is True

    def test_validate_cpf_invalid_format(self, person_service):
        invalid_cpf = "123.456.789"
        with pytest.raises(InvalidCPFError, match="Invalid CPF format"):
            person_service.validate_cpf(invalid_cpf)

    def test_validate_cpf_invalid_number(self, person_service):
        invalid_cpf = "123.456.789-00"
        with pytest.raises(InvalidCPFError, match="Invalid CPF number"):
            person_service.validate_cpf(invalid_cpf)

    def test_validate_cpf_repeated_digits(self, person_service):
        invalid_cpf = "111.111.111-11"
        with pytest.raises(InvalidCPFError, match="Invalid CPF format"):
            person_service.validate_cpf(invalid_cpf)

    def test_validate_cnpj_valid(self, person_service):
        valid_cnpj = "11.222.333/0001-81"
        assert person_service.validate_cnpj(valid_cnpj) is True

    def test_validate_cnpj_invalid_format(self, person_service):
        invalid_cnpj = "11.222.333/0001"
        with pytest.raises(InvalidCNPJError, match="Invalid CNPJ format"):
            person_service.validate_cnpj(invalid_cnpj)

    def test_validate_cnpj_invalid_number(self, person_service):
        invalid_cnpj = "11.222.333/0001-00"
        with pytest.raises(InvalidCNPJError, match="Invalid CNPJ number"):
            person_service.validate_cnpj(invalid_cnpj)

    def test_validate_cnpj_repeated_digits(self, person_service):
        invalid_cnpj = "11111111111111"
        with pytest.raises(InvalidCNPJError, match="Invalid CNPJ format"):
            person_service.validate_cnpj(invalid_cnpj)
