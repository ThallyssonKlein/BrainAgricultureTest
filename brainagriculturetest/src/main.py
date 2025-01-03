from fastapi import FastAPI

# Instância da aplicação FastAPI
app = FastAPI()

# Including FarmerController
from brainagriculturetest.src.ports.inbound.http.controllers.farmer_controller import FarmerController
from brainagriculturetest.src.adapters.inbound.http.farmer_adapter import FarmerAdapter

from brainagriculturetest.src.ports.outbound.database.farm.outbound_farm_repository_port import OutboundFarmRepositoryPort
from brainagriculturetest.src.domain.farm.farm_service import FarmService

farm_adapter = FarmerAdapter(OutboundFarmRepositoryPort(), FarmService())
farmer_controller = FarmerController(farm_adapter)

app.include_router(farmer_controller.get_router())

