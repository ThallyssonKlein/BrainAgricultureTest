from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort
from shared.loggable import Loggable

class CultureService(Loggable):
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort):
        Loggable.__init__(self, prefix="CultureService")
        self.outbound_culture_repository_port = outbound_culture_repository_port
    
    async def __validate_culture_exists(self, farmer_id, culture_data: dict, trace_id: str, update=False):
        self.log.info(f"Creating culture for farmer with id: {farmer_id} and data: {culture_data}", trace_id)
        culture = None

        if not update:
            culture = await self.outbound_culture_repository_port.get_by_farmer_id_and_name(farmer_id, culture_data["name"], trace_id)
        else:
            culture = await self.outbound_culture_repository_port.get_by_farmer_id_and_name(farmer_id, culture_data["old_name"], trace_id)

        if culture:
            self.log.error(f"Culture with name {culture_data['name']} already exists for farmer with id {farmer_id}", trace_id)
            raise CultureAlreadyExistsError()

    async def create_culture_for_a_farmer(self, farmer_id, culture_data: dict, trace_id: str):
        await self.__validate_culture_exists(farmer_id, culture_data, trace_id)
        self.log.info(f"Creating culture for farmer with id: {farmer_id} and data: {culture_data}", trace_id)
        return await self.outbound_culture_repository_port.create_culture_for_a_farmer(farmer_id, culture_data)
    
    async def update_culture_by_id(self, farmer_id, culture_data: dict, trace_id: str):
        await self.__validate_culture_exists(farmer_id, culture_data, trace_id, True)
        self.log.info(f"Updating culture for farmer with id: {farmer_id} and data: {culture_data}", trace_id)
        return await self.outbound_culture_repository_port.update_culture_by_id(farmer_id, culture_data, trace_id)