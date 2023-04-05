import unittest

from services.pre_diagnostic_service import PreDiagnosticService


class TestPreDiagnosticService(unittest.TestCase):

    def setUp(self) -> None:
        self.service = PreDiagnosticService()

    def test_pre_diagnostic_tem_febre(self):
        input_request = "Estou com febre"
        expected_response = "Você apresenta diversos sintomas de Covid"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)

    def test_pre_diagnostic_case(self):
        input_request = "Estou com FEBRE"
        expected_response = "Você apresenta diversos sintomas de Covid"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)
        input_request = "Estou com febre"
        expected_response = "Você apresenta diversos sintomas de Covid"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)

    def test_pre_diagnostic_tem_tosse_seca(self):
        input_request = "Estou com Tosse seca"
        expected_response = "Você apresenta diversos sintomas de Covid"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)

    def test_pre_diagnostic_tem_febre(self):
        input_request = "Estou bem"
        expected_response = "Você não apresenta sintomas de Covid"

        result_response = self.service.get_pre_diagnostic(input_request)

        self.assertEqual(expected_response, result_response)
