from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from domain.farm.invalid_area_error import InvalidAreaError

class FarmService:
    def __init__(self, outbound_farm_repository_port: OutboundFarmRepositoryPort):
        self.outbound_farm_repository_port = outbound_farm_repository_port

    async def create_farm(self, farmer_id, farm_data):
        if farm_data['arable_area'] + farm_data['vegetation_area'] != farm_data['total_area']:
            raise InvalidAreaError("The sum of arable and vegetation area cannot be greater than the total area")
        
        return (await self.outbound_farm_repository_port.create_farm(farmer_id, farm_data))