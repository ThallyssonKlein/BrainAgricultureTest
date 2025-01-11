from adapters.inbound.http.schemas import FarmerSchema
from ports.inbound.http.error.conflict_error import ConflictError
from domain.farm.farm_service import FarmService
from domain.farm.invalid_area_error import InvalidAreaError
from domain.person.invalid_cnpj_error import InvalidCNPJError
from domain.person.invalid_cpf_error import InvalidCPFError
from domain.person.person_service import PersonService
from ports.inbound.http.error.bad_request_error import BadRequestError
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

    async def create_farmer(self, farmer_schema: FarmerSchema):
        farmer_data = farmer_schema.dict()

        try:
            if len(farmer_data['document']) == 11:
                self.person_service.validate_cpf(farmer_data['document'])
            else:
                self.person_service.validate_cnpj(farmer_data['document'])
        except InvalidCPFError as err:
            raise BadRequestError(err)
        except InvalidCNPJError as err:
            raise BadRequestError(err)
        
        # Step 1: Create Farmer
        farmer = None

        try:
            farmer = await self.outbound_farmer_repository_port.create_farmer(farmer_data)
        # Validate if the error is the farmer with the same id
        except IntegrityError as err:
            if err._message().find("duplicate key value violates unique constraint") != -1:
                raise ConflictError("Farmer already exists")

        # Step 2: Iterate over farms
        for farm_data in farmer_data["farms"]:
            farm = None
            try:
                farm = await FarmService.create_farm(self, farmer.id, farm_data)
            except InvalidAreaError as err:
                await self.outbound_farmer_repository_port.delete_farmer(farmer.id)
                raise BadRequestError(err.get_message)
            except Exception as err:
                await self.outbound_farmer_repository_port.delete_farmer(farmer.id)
                raise err

            # Step 3: Iterate over crops in each farm
            for crop_data in farm_data["crops"]:
                # Step 4: Get or create the culture
                culture = None
                try:
                    culture = await self.outbound_culture_repository_port.get_or_create_culture(crop_data["culture"]["name"])
                except Exception as err:
                    await self.outbound_farm_repository_port.delete_farm(farm.id)
                    await self.outbound_farmer_repository_port.delete_farmer(farmer.id)
                    raise err

                # Step 5: Create crop with the associated culture
                try:
                    await self.outbound_crop_repository_port.create_crop(farm.id, crop_data, culture.id)
                except Exception as err:
                    await self.outbound_culture_repository_port.delete_culture(culture.id)
                    await self.outbound_farm_repository_port.delete_farm(farm.id)
                    await self.outbound_farmer_repository_port.delete_farmer(farmer.id)
                    raise err
                    

        return self.outbound_farmer_repository_port.get_farm_relations(farmer.id)

    async def find_farmers_paginated_and_with_query(self, limit: int, offset: int, query: str):
        return await self.outbound_farmer_repository_port.find_farmers_paginated_and_with_query(limit, offset, query)