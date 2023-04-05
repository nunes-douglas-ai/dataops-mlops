from pydantic import BaseModel


class PreDiagnosticRequest(BaseModel):
    name: str
    text: str


class PreDiagnosticResponse(BaseModel):
    name: str
    diagnostic: str
