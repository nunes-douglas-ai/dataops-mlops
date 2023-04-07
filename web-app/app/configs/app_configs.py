from pydantic import BaseSettings


class AppSettings(BaseSettings):
    port: int = 8000
    log_level: str = "debug"
    workers: int = 1

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = "mongo_user"
    mongo_pass: str = "mongo_pass"
    mongo_database_name: str = "covid_app"
    mongo_export_collection_name: str = "requests_staging"
