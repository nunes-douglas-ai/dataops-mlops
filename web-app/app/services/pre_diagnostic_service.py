from fastapi import HTTPException

from configs.app_configs import AppSettings
from entities.pre_diagnostic_entities import PreDiagnosticResponse
from services.model_loader import ModelLoader
from utils.version import __version__


class PreDiagnosticService:

    def __init__(self, app_settings: AppSettings = AppSettings()):
        self.app_settings = app_settings
        self.model_name = app_settings.mlflow_model_name
        self.model_stage = app_settings.mlflow_model_stage
        self.model_loader = ModelLoader(app_settings)

    @staticmethod
    def get_pre_diagnostic(model, input_text):
        return model._predict_fn([input_text])[0]

    def process_diagnostic(self, request):
        model_version = request.model_version
        try:
            model = self.model_loader.get_model(version=model_version)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=str(exc.args)
            )

        symptons = request.text
        diagnostic = self.get_pre_diagnostic(model, symptons)

        return PreDiagnosticResponse(
            name=request.name,
            diagnostic=diagnostic,
            version=__version__,
            model_name=self.model_name,
            model_id=model.metadata.run_id
        )
