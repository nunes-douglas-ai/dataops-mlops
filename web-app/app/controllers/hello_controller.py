from fastapi import APIRouter

hello_router = APIRouter()


@hello_router.get("/talk")
async def talk():
    return {
        "message": "Olá mundo!"
    }
