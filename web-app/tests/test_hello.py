import unittest

from entities.hello_entities import HelloRequest, HelloResponse
from services.hello_service import HelloService


class TestHelloService(unittest.TestCase):

    def setUp(self) -> None:
        self.service = HelloService()

    def test_process_talk(self):
        input_request = HelloRequest(name="Douglas")
        expected_response = HelloResponse(message="Olá Douglas!")

        result_response = self.service.process_talk(input_request)

        self.assertEqual(expected_response, result_response)
