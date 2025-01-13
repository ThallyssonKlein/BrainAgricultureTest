from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.error.conflict_error import ConflictError
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

from shared.loggable import Loggable

class InboundFarmerAdapter(Loggable):
    def __init__(self, outbound_farmer_repository_port: OutboundFarmerRepositoryPort, 
                 person_service: PersonService,
                 outbound_culture_repository_port: OutboundCultureRepositoryPort,
                 outbound_crop_repository_port: OutboundCropRepositoryPort,
                 outbound_farm_repository_port: OutboundFarmRepositoryPort):
        Loggable.__init__(self, prefix="InboundFarmerAdapter")
        self.outbound_farmer_repository_port = outbound_farmer_repository_port
        self.person_service = person_service
        self.outbound_culture_repository_port = outbound_culture_repository_port
        self.outbound_crop_repository_port = outbound_crop_repository_port
        self.outbound_farm_repository_port = outbound_farm_repository_port

    def __farmer_validations(self, farmer_data, trace_id: str):
        try:
            if len(farmer_data['document']) == 11:
                self.log.info(f"Validating CPF: {farmer_data['document']}", trace_id)
                self.person_service.validate_cpf(farmer_data['document'])
            else:
                self.log.info(f"Validating CNPJ: {farmer_data['document']}", trace_id)
                self.person_service.validate_cnpj(farmer_data['document'])
        except InvalidCPFError as err:
            self.log.error(err.get_message, trace_id)
            raise BadRequestError(err.get_message)
        except InvalidCNPJError as err:
            self.log.error(err.get_message, trace_id)
            raise BadRequestError(err.get_message)


    async def create_farmer(self, farmer_schema: FarmerSchema, trace_id: str):
        farmer_data = farmer_schema.model_dump()
        
        self.__farmer_validations(farmer_data, trace_id)

        try:
            self.log.info(f"Creating farmer with data: {farmer_data}", trace_id)
            farmer = await self.outbound_farmer_repository_port.create_farmer(farmer_data, trace_id)
            return farmer
        except IntegrityError as err:
            self.log.error(err._message(), trace_id)
            if err._message().find("duplicate key value violates unique constraint") != -1:
                raise ConflictError("Farmer already exists")
    
    async def update_farmer(self, farmer_id: int, farmer_schema: FarmerSchema, trace_id: str):
        farmer_data = farmer_schema.model_dump()
        farmer_data['id'] = farmer_id

        self.__farmer_validations(farmer_data, trace_id)

        try:
            self.log.info(f"Updating farmer with id: {farmer_id} and data: {farmer_data}", trace_id)
            farmer = await self.outbound_farmer_repository_port.update_farmer(farmer_data, trace_id)
            return farmer
        except ValueError as err:
            if err.args[0] == "Farmer not found":
                self.log.error("Farmer not found", trace_id)
                raise NotFoundError("Farmer not found")

    async def find_farmers_paginated_and_with_query(self, limit: int, offset: int, query: str, trace_id: str):
        self.log.info(f"Finding farmers with limit: {limit}, offset: {offset}, query: {query}", trace_id)
        return await self.outbound_farmer_repository_port.find_farmers_paginated_and_with_query(limit, offset, query, trace_id)
    
    async def delete_farmer_by_id(self, farmer_id: int, trace_id: str):
        self.log.info(f"Deleting farmer with id: {farmer_id}", trace_id)
        result = await self.outbound_farmer_repository_port.delete_farmer_by_id(farmer_id, trace_id)
        if result.rowcount == 0:
            self.log.error("Farmer not found", trace_id)
            raise NotFoundError("Farmer not found")