from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.error.conflict_error import ConflictError
from domain.farm.farm_service import FarmService
from domain.farm.invalid_area_error import InvalidAreaError
from domain.person.invalid_cnpj_error import InvalidCNPJError
from domain.person.invalid_cpf_error import InvalidCPFError
from domain.person.person_service import PersonService
from ports.inbound.http.error.bad_request_error import BadRequestError
from ports.inbound.http.error.not_found_error import NotFoundError
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from ports.outbound.database.outbound_farmer_repository_port import OutboundFarmerRepositoryPort
from sqlalchemy.exc import IntegrityError

class InboundFarmerAdapter:
    def __init__(self, outbound_farmer_repository_port: OutboundFarmerRepositoryPort, 
                 farm_service: FarmService, person_service: PersonService,
                 outbound_culture_repository_port: OutboundCultureRepositoryPort,
                 outbound_crop_repository_port: OutboundCropRepositoryPort,
                 outbound_farm_repository_port: OutboundFarmRepositoryPort):
        self.outbound_farmer_repository_port = outbound_farmer_repository_port
        self.farm_service = farm_service
        self.person_service = person_service
        self.outbound_culture_repository_port = outbound_culture_repository_port
        self.outbound_crop_repository_port = outbound_crop_repository_port
        self.outbound_farm_repository_port = outbound_farm_repository_port

    def __farmer_validations(self, farmer_data):
        try:
            if len(farmer_data['document']) == 11:
                self.person_service.validate_cpf(farmer_data['document'])
            else:
                self.person_service.validate_cnpj(farmer_data['document'])
        except InvalidCPFError as err:
            raise BadRequestError(err)
        except InvalidCNPJError as err:
            raise BadRequestError(err)


    async def create_farmer(self, farmer_schema: FarmerSchema):
        farmer_data = farmer_schema.dict()
        
        self.__farmer_validations(farmer_data)

        try:
            farmer = await self.outbound_farmer_repository_port.create_farmer(farmer_data)
            return farmer
        except IntegrityError as err:
            if err._message().find("duplicate key value violates unique constraint") != -1:
                raise ConflictError("Farmer already exists")
    
    async def update_farmer(self, farmer_id: int, farmer_schema: FarmerSchema):
        farmer_data = farmer_schema.dict()
        farmer_data['id'] = farmer_id

        self.__farmer_validations(farmer_data)

        try:
            farmer = await self.outbound_farmer_repository_port.update_farmer(farmer_data)
            return farmer
        except ValueError as err:
            if err._message().find("Farmer not found with the provided id") != -1:
                raise NotFoundError("Farmer not found with the provided id")

    async def find_farmers_paginated_and_with_query(self, limit: int, offset: int, query: str):
        return await self.outbound_farmer_repository_port.find_farmers_paginated_and_with_query(limit, offset, query)
    
    async def delete_farmer_by_id(self, farmer_id: int):
        await self.outbound_farmer_repository_port.delete_farmer_by_id(farmer_id)