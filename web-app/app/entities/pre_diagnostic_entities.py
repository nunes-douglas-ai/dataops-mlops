from enum import Enum

from pydantic import BaseModel


class AvailableOutputs(str, Enum):
    POSITIVO = "positivo"
    NEGATIVO = "negativo"


class PreDiagnosticRequest(BaseModel):
    name: str
    text: str


class PreDiagnosticResponse(BaseModel):
    name: str
    diagnostic: str
