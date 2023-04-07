from fastapi import FastAPI

from controllers.hello_controller import hello_router
from controllers.pre_diagnostic_controller import pre_diagnostic_router
from services.data_exporter import DataExporter

__version__ = "0.5.0"

app = FastAPI(
    title="Meu projeto de DataOps e MlOps",
    version=__version__,
    description="Projeto simples para demonstrar conceitos de DevOps, DataOps e MlOps"
)
app.include_router(hello_router)
app.include_router(pre_diagnostic_router)

app.add_middleware(DataExporter)
