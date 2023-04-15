from typing import Optional

from pydantic import BaseModel


class PreDiagnosticRequest(BaseModel):
    name: str
    text: str
    extra_args: Optional[dict] = None


class PreDiagnosticResponse(BaseModel):
    name: str
    diagnostic: str
    model_used: str
