from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from adapters.inbound.http.inbound_crop_adapter import InboundCropAdapter
from adapters.inbound.http.inbound_culture_adapter import InboundCultureAdapter
from adapters.inbound.http.inbound_dashboard_adapter import InboundDashboardAdapter
from adapters.inbound.http.inbound_farm_adapter import InboundFarmAdapter
from ports.inbound.http.controllers.crop_controller import CropController
from ports.inbound.http.controllers.culture_controller import CultureController
from ports.inbound.http.controllers.dashboard_controller import DashboardController
from ports.inbound.http.controllers.farm_controller import FarmController
from ports.inbound.http.error.http_error import HttpError
from ports.inbound.http.controllers.farmer_controller import FarmerController
from adapters.inbound.http.inbound_farmer_adapter import InboundFarmerAdapter

from ports.outbound.database.outbound_farmer_repository_port import OutboundFarmerRepositoryPort
from ports.outbound.database.outbound_farm_repository_port import OutboundFarmRepositoryPort
from ports.outbound.database.outbound_crop_repository_port import OutboundCropRepositoryPort
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort
from domain.farm.farm_service import FarmService
from domain.person.person_service import PersonService
from ports.outbound.database.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def init_dependencies(db: AsyncSession):

    outbound_farmer_repository_port = OutboundFarmerRepositoryPort(db)
    outbound_culture_repository_port = OutboundCultureRepositoryPort(db)
    outbound_crop_repository_port = OutboundCropRepositoryPort(db)
    outbound_farm_repository_port = OutboundFarmRepositoryPort(db)

    inbound_farmer_adapter = InboundFarmerAdapter(
        outbound_farmer_repository_port,
        FarmService(outbound_farm_repository_port),
        PersonService(),
        outbound_culture_repository_port,
        outbound_crop_repository_port,
        outbound_farm_repository_port
    )

    inbound_dashboard_adapter = InboundDashboardAdapter(outbound_farm_repository_port)
    inbound_farm_adapter = InboundFarmAdapter(outbound_farm_repository_port)
    inbound_crop_adapter = InboundCropAdapter(outbound_crop_repository_port)
    inbound_culture_adapter = InboundCultureAdapter(outbound_culture_repository_port)

    return inbound_farmer_adapter, inbound_dashboard_adapter, inbound_farm_adapter, inbound_crop_adapter, inbound_culture_adapter


# Resolver dependências
async def get_farmer_adapter() -> InboundFarmerAdapter:
    async for db in get_db():
        return await init_dependencies(db)

# Instanciar o controller
async def init_app():
    inbound_farmer_adapter, inbound_dashboard_adapter, inbound_farm_adapter, inbound_crop_adapter, inbound_culture_adapter = await get_farmer_adapter()
    farmer_controller = FarmerController(inbound_farmer_adapter)
    dashboard_controller = DashboardController(inbound_dashboard_adapter)
    farm_controller = FarmController(inbound_farm_adapter)
    crop_controller = CropController(inbound_crop_adapter)
    culture_controller = CultureController(inbound_culture_adapter)

    # Incluir o router do controller
    app.include_router(farmer_controller.get_router())
    app.include_router(dashboard_controller.get_router())
    app.include_router(farm_controller.get_router())
    app.include_router(crop_controller.get_router())
    app.include_router(culture_controller.get_router())

import asyncio
asyncio.run(init_app())

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





