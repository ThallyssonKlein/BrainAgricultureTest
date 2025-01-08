from brainagriculturetest.src.domain.person.invalid_cnpj_error import InvalidCNPJError
from brainagriculturetest.src.domain.person.invalid_cpf_error import InvalidCPFError


class PersonService:
    def validate_cpf(cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise InvalidCPFError("Invalid CPF format")

        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                raise InvalidCPFError("Invalid CPF number")

        return True

def validate_cnpj(cnpj: str) -> bool:
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        raise InvalidCNPJError("Invalid CNPJ format")

    def calculate_digit(cnpj, digit):
        if digit == 1:
            weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        else:
            weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        value = sum(int(cnpj[i]) * weights[i] for i in range(len(weights)))
        digit = 11 - (value % 11)
        return digit if digit < 10 else 0

    if calculate_digit(cnpj, 1) != int(cnpj[12]) or calculate_digit(cnpj, 2) != int(cnpj[13]):
        raise InvalidCNPJError("Invalid CNPJ number")

    return True
