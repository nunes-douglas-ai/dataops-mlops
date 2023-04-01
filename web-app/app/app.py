from fastapi import FastAPI

from controllers.hello_controller import hello_router

app = FastAPI()
app.include_router(hello_router)
