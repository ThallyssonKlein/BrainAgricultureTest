from adapters.inbound.http.schemas import CultureSchema
from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from domain.culture.culture_service import CultureService
from ports.inbound.http.error.conflict_error import ConflictError
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort


class InboundCultureAdapter:
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort, culture_service: CultureService):
        self.outbound_culture_repository_port = outbound_culture_repository_port
        self.culture_service = culture_service

    async def create_culture_for_a_farmer(self, farmer_id: int, culture: CultureSchema):
        c = culture.dict()
        try:
            return await self.culture_service.create_culture_for_a_farmer(farmer_id, c)
        except CultureAlreadyExistsError as err:
            raise ConflictError(err.get_message)
    
    async def get_cultures_for_a_farmer_id(self, farmer_id: int):
        return await self.outbound_culture_repository_port.get_cultures_for_a_farmer_id(farmer_id)

    async def update_culture_by_id(self, culture_id: int, culture: dict):
        return await self.outbound_culture_repository_port.update_culture_by_id(culture_id, culture)
    
    async def delete_culture_by_id(self, culture_id: int):
        try:
            return await self.outbound_culture_repository_port.delete_culture_by_id(culture_id)
        except Exception as err:
            if "violates foreign key constraint" in str(err):
                raise ConflictError("This culture is being used by a crop")