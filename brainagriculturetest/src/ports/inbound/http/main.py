from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from brainagriculturetest.src.ports.inbound.http.error.http_error import HttpError
from brainagriculturetest.src.ports.outbound.database.farm.outbound_farm_repository_port import OutboundFarmRepositoryPort

# Instância da aplicação FastAPI
app = FastAPI()

# Including FarmerController
from brainagriculturetest.src.ports.inbound.http.controllers.farmer_controller import FarmerController
from brainagriculturetest.src.adapters.inbound.http.farmer_adapter import FarmerAdapter

from brainagriculturetest.src.ports.outbound.database.farmer.outbound_farmer_repository_port import OutboundFarmerRepositoryPort
from brainagriculturetest.src.domain.farm.farm_service import FarmService

farm_adapter = FarmerAdapter(OutboundFarmerRepositoryPort(), FarmService(OutboundFarmRepositoryPort()))
farmer_controller = FarmerController(farm_adapter)

app.include_router(farmer_controller.get_router())

@app.exception_handler(HttpError)
async def http_error_handler(request: Request, exc: HttpError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"},
    )







