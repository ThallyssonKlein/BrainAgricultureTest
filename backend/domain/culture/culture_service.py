from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort

class CultureService:
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort):
        self.outbound_culture_repository_port = outbound_culture_repository_port
    
    async def create_culture_for_a_farmer(self, farmer_id, culture_data: dict):
        culture = await self.outbound_culture_repository_port.get_by_farmer_id_and_name(farmer_id, culture_data["name"])

        if culture:
            raise CultureAlreadyExistsError()

        return await self.outbound_culture_repository_port.create_culture_for_a_farmer(farmer_id, culture_data)