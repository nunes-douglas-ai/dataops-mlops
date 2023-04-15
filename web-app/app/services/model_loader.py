import os.path
import pickle

from sklearn.pipeline import Pipeline

from configs.app_configs import AppSettings


class ModelLoader:

    def __init__(self, app_settings: AppSettings = AppSettings()):
        self.app_settings = app_settings
        self.models_path = app_settings.models_path

    def get_model(self, model_name) -> Pipeline:
        model_path = os.path.join(self.models_path, model_name)
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        return model
