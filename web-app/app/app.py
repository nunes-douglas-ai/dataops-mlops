from fastapi import FastAPI

from controllers.hello_controller import hello_router

__version__ = "0.4.1"

app = FastAPI(
    title="Meu projeto de DataOps e MlOps",
    version=__version__,
    description="Projeto simples para demonstrar conceitos de DevOps, DataOps e MlOps"
)
app.include_router(hello_router)
