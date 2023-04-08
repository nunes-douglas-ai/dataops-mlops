from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AvailableOutputs(str, Enum):
    POSITIVO = "positivo"
    NEGATIVO = "negativo"


class PreDiagnosticRequest(BaseModel):
    name: str
    text: str
    extra_args: Optional[dict] = None


class PreDiagnosticResponse(BaseModel):
    name: str
    diagnostic: str
