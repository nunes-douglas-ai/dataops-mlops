from pydantic import BaseSettings


class AppSettings(BaseSettings):
    port: int = 8000
    log_level: str = "debug"
    workers: int = 1
