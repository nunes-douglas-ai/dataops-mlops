from urllib.parse import quote_plus

import pymongo

from configs.app_configs import AppSettings


class RequestsRepository:

    def __init__(self, app_settings: AppSettings = AppSettings()):
        self.app_settings = app_settings
        mongo_url = RequestsRepository._create_mongo_url(
            username=app_settings.mongo_user,
            password=app_settings.mongo_pass,
            hostname=app_settings.mongo_host,
            port=app_settings.mongo_port,
            database_name=app_settings.mongo_database_name
        )
        self.collection_name = app_settings.mongo_export_collection_name
        self.client = pymongo.MongoClient(mongo_url)

    @staticmethod
    def _create_mongo_url(username: str, password: str, hostname: str, port: int, database_name: str):
        return f'mongodb://{quote_plus(username)}:{quote_plus(password)}@{hostname}:{port}/{database_name}?authSource=admin'

    def add_request(self, request_data):
        db = self.client.get_database()
        collection = db[self.collection_name]
        collection.insert_one(dict(request_data))
