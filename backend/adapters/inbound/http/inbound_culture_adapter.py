from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort


class InboundCultureAdapter:
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort):
        self.outbound_culture_repository_port = outbound_culture_repository_port

    async def create_culture_for_a_farmer_id(self, farmer_id: int, culture: dict):
        return await self.outbound_culture_repository_port.create_culture_for_a_farmer_id(farmer_id, culture)