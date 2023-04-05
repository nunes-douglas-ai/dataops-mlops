from fastapi import FastAPI

from controllers.hello_controller import hello_router
from controllers.pre_diagnostic_controller import pre_diagnostic_router

__version__ = "0.4.3"

app = FastAPI(
    title="Meu projeto de DataOps e MlOps",
    version=__version__,
    description="Projeto simples para demonstrar conceitos de DevOps, DataOps e MlOps"
)
app.include_router(hello_router)
app.include_router(pre_diagnostic_router)
