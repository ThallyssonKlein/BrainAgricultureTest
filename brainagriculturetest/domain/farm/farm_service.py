from domain.farm.invalid_area_error import InvalidAreaError

class FarmService:
    def __init__(self, outbound_farm_repository_port):
        self.outbound_farm_repository_port = outbound_farm_repository_port

    def create_farm(self, farm_data):
        if farm_data.arable_area + farm_data.vegetation_area > farm_data.total_area:
            raise InvalidAreaError("The sum of arable and vegetation area cannot be greater than the total area")
        
        return self.outbound_farm_repository_port.create_farm(farm_data).id