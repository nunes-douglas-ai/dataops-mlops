from typing import Optional

from pydantic import BaseModel


class PreDiagnosticRequest(BaseModel):
    name: str
    text: str
    extra_args: Optional[dict] = None
    model_version: Optional[int] = None


class PreDiagnosticResponse(BaseModel):
    name: str
    diagnostic: str
    version: str
    model_name: str
    model_id: str
