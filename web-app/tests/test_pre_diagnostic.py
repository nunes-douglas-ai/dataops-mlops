import unittest

from configs.app_configs import AppSettings
from services.pre_diagnostic_service import PreDiagnosticService


class TestPreDiagnosticService(unittest.TestCase):

    def setUp(self) -> None:
        self.app_setings = AppSettings()
        self.app_setings.models_path = "models"
        self.service = PreDiagnosticService(self.app_setings)

    def test_pre_diagnostic_tem_febre(self):
        input_request = "Estou com febre"
        expected_response = "positivo"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)

    def test_pre_diagnostic_case(self):
        input_request = "Estou com FEBRE"
        expected_response = "positivo"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)
        input_request = "Estou com febre"
        expected_response = "positivo"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)

    def test_pre_diagnostic_tem_tosse_seca(self):
        input_request = "Estou com Tosse seca"
        expected_response = "positivo"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)

    def test_pre_diagnostic_sem_sintomas(self):
        input_request = "Estou bem"
        expected_response = "negativo"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)
