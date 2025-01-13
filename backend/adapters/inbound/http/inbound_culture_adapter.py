from adapters.inbound.http.schemas import CultureSchema
from domain.culture.culture_already_exists_error import CultureAlreadyExistsError
from domain.culture.culture_service import CultureService
from ports.inbound.http.error.conflict_error import ConflictError
from ports.inbound.http.error.not_found_error import NotFoundError
from ports.outbound.database.outbound_culture_repository_port import OutboundCultureRepositoryPort
from shared.loggable import Loggable

class InboundCultureAdapter(Loggable):
    def __init__(self, outbound_culture_repository_port: OutboundCultureRepositoryPort, culture_service: CultureService):
        Loggable.__init__(self, prefix="InboundCultureAdapter")
        self.outbound_culture_repository_port = outbound_culture_repository_port
        self.culture_service = culture_service

    async def create_culture_for_a_farmer(self, farmer_id: int, culture: CultureSchema, trace_id: str):
        c = culture.model_dump()
        try:
            self.log.info(f"Creating culture for farmer with id: {farmer_id} and data: {c}", trace_id)
            return await self.culture_service.create_culture_for_a_farmer(farmer_id, c, trace_id)
        except CultureAlreadyExistsError as err:
            self.log.error(err.get_message, trace_id)
            raise ConflictError(err.get_message)
    
    async def get_cultures_for_a_farmer(self, farmer_id: int, trace_id: str):
        self.log.info(f"Getting cultures for farmer with id: {farmer_id}", trace_id)
        return await self.outbound_culture_repository_port.get_cultures_for_a_farmer(farmer_id, trace_id)

    async def update_culture_by_id(self, culture_id: int, culture: CultureSchema, trace_id: str):
        c = culture.model_dump()
        try:
            self.log.info(f"Updating culture with id: {culture_id} and data: {c}", trace_id)
            return await self.culture_service.update_culture_by_id(culture_id, c, trace_id)
        except ValueError as err:
            if err.args[0] == "Culture not found":
                self.log.error("Culture not found", trace_id)
                raise NotFoundError("Culture not found")
        except CultureAlreadyExistsError as err:
            self.log.error(err.get_message, trace_id)
            raise ConflictError(err.get_message)
    
    async def delete_culture_by_id(self, culture_id: int, trace_id: str):
        result = None
        try:
            self.log.info(f"Deleting culture with id: {culture_id}", trace_id)
            result = await self.outbound_culture_repository_port.delete_culture_by_id(culture_id, trace_id)
        except Exception as err:
            self.log.error(str(err), trace_id)
            if "violates foreign key constraint" in str(err):
                raise ConflictError("This culture is being used by a crop")
        if result.rowcount == 0:
            self.log.error("Culture not found", trace_id)
            raise NotFoundError("Culture not found")
