class FarmerAdapter:
    def __init__(self, outbound_farmer_repository_port, farm_service):
        self.outbound_farmer_repository_port = outbound_farmer_repository_port
        self.farm_service = farm_service

    def create_farmer(self, farmer_data):
        self.farm_service.create_farm(farmer_data["farm"])