from pydantic import BaseModel


class HelloRequest(BaseModel):
    name: str


class HelloResponse(BaseModel):
    message: str
