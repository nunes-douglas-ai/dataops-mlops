import mlflow
from cachetools import cached, TTLCache
from mlflow.pyfunc import PyFuncModel

from configs.app_configs import AppSettings


class ModelLoader:

    def __init__(self, app_settings: AppSettings = AppSettings()):
        self.app_settings = app_settings
        self.ml_flow_model_name = app_settings.mlflow_model_name
        self.ml_flow_model_stage = app_settings.mlflow_model_stage
        mlflow.set_tracking_uri(app_settings.mlflow_host)

    @cached(cache=TTLCache(maxsize=32, ttl=60))
    def get_model(self, version=None) -> PyFuncModel:
        if version is not None:
            return mlflow.pyfunc.load_model(model_uri=f"models:/{self.ml_flow_model_name}/{version}")
        return mlflow.pyfunc.load_model(model_uri=f"models:/{self.ml_flow_model_name}/{self.ml_flow_model_stage}")
