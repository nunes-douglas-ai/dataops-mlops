from fastapi import APIRouter

from entities.pre_diagnostic_entities import PreDiagnosticRequest, PreDiagnosticResponse
from services.pre_diagnostic_service import PreDiagnosticService

pre_diagnostic_router = APIRouter(prefix="/pre-diagnostic", tags=["devops"])

service = PreDiagnosticService()


@pre_diagnostic_router.post("/process-diagnostic")
async def talk(request: PreDiagnosticRequest) -> PreDiagnosticResponse:
    return service.process_diagnostic(request)
