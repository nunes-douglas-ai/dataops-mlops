from fastapi import APIRouter

from entities.hello_entities import HelloResponse, HelloRequest
from services.hello_service import HelloService

hello_router = APIRouter(prefix="/hello", tags=["hello"])

service = HelloService()


@hello_router.post("/talk")
async def talk(request: HelloRequest) -> HelloResponse:
    return service.process_talk(request)
