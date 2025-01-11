from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort

class InboundFarmAdapter:
    def __init__(self, outbound_farm_repository_port: OutboundFarmRepositoryPort):
        self.outbound_farm_repository_port = outbound_farm_repository_port

    async def find_farms_by_state_and_farmer_id(self, farmer_id: int, state: str):
        return await self.outbound_farm_repository_port.find_farms_by_state_and_farmer_id(farmer_id, state)