from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from domain.person.person_service import PersonService
from ports.inbound.http.error.http_error import HttpError
from ports.outbound.database.db import get_db
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort

# Instância da aplicação FastAPI
app = FastAPI()

# Including FarmerController
from ports.inbound.http.controllers.farmer_controller import FarmerController
from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter

from ports.outbound.database.outbound_farmer_repository_port import OutboundFarmerRepositoryPort
from domain.farm.farm_service import FarmService

def get_farm_adapter(db: AsyncSession = Depends(get_db)):
    return InboundFarmerAdapter(
        OutboundFarmerRepositoryPort(db),
        FarmService(
            OutboundFarmRepositoryPort(db),
            PersonService(),
            OutboundCultureRepositoryPort(db),
            OutboundCropRepositoryPort(db),
            OutboundFarmRepositoryPort(db)
        )
    )

farmer_controller = FarmerController(get_farm_adapter)

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







