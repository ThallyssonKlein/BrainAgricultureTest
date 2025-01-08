from brainagriculturetest.src.domain.farm.farm_service import FarmService
from brainagriculturetest.src.domain.farm.invalid_area_error import InvalidAreaError
from brainagriculturetest.src.domain.person.invalid_cnpj_error import InvalidCNPJError
from brainagriculturetest.src.domain.person.invalid_cpf_error import InvalidCPFError
from brainagriculturetest.src.domain.person.person_service import PersonService
from brainagriculturetest.src.ports.inbound.http.error.bad_request_error import BadRequestError
from brainagriculturetest.src.ports.outbound.database.farmer.outbound_farmer_repository_port import OutboundFarmerRepositoryPort

class FarmerAdapter:
    def __init__(self, outbound_farmer_repository_port: OutboundFarmerRepositoryPort, farm_service: FarmService, person_service: PersonService):
        self.outbound_farmer_repository_port = outbound_farmer_repository_port
        self.farm_service = farm_service
        self.person_service = person_service

    def create_farmer(self, farmer_data):
        try:
            if len(farmer_data['document']) == 11:
                self.person_service.validate_cpf(farmer_data['document'])
            else:
                self.person_service.validate_cnpj(farmer_data['document'])
        except InvalidCPFError as err:
            raise BadRequestError(err)
        except InvalidCNPJError as err:
            raise BadRequestError(err)

        farm_ids = []
        try:
            for farm in farmer_data['farms']:
                farm_ids.append(self.farm_service.create_farm(farm))
        except InvalidAreaError as err:
            raise BadRequestError(err)