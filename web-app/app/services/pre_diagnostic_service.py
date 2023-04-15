from configs.app_configs import AppSettings
from entities.pre_diagnostic_entities import PreDiagnosticResponse
from services.model_loader import ModelLoader


class PreDiagnosticService:

    def __init__(self, app_settings: AppSettings = AppSettings()):
        self.app_settings = app_settings
        self.model_file_name = app_settings.model_file_name
        self.model_loader = ModelLoader(app_settings)
        self.model = self.model_loader.get_model(self.model_file_name)

    def get_pre_diagnostic(self, input_request):
        return self.model.predict([input_request])[0]

    def process_diagnostic(self, request):
        symptons = request.text
        diagnostic = self.get_pre_diagnostic(symptons)
        return PreDiagnosticResponse(
            name=request.name,
            diagnostic=diagnostic,
            model_used=self.model_file_name
        )
