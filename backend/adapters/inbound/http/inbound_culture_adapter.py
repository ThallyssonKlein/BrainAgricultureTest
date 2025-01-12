from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from domain.culture.culture_service import CultureService
from ports.inbound.http.error.conflict_error import ConflictError
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort


class InboundCultureAdapter:
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort, culture_service: CultureService):
        self.outbound_culture_repository_port = outbound_culture_repository_port
        self.culture_service = culture_service

    async def create_culture_for_a_farmer_id(self, farmer_id: int, culture: dict):
        try:
            return await self.culture_service.create_culture_for_a_farmer_id(farmer_id, culture)
        except CultureAlreadyExistsError as err:
            raise ConflictError(err.get_message)
    
    async def get_cultures_for_a_farmer_id(self, farmer_id: int):
        return await self.outbound_culture_repository_port.get_cultures_for_a_farmer_id(farmer_id)