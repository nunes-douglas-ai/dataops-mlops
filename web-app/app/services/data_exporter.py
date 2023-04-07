from datetime import datetime

from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Message

from configs.app_configs import AppSettings
from repositories.requests_repository import RequestsRepository
from utils.logger import app_logger


class DataExporter(BaseHTTPMiddleware):

    def __init__(self, app, app_settings: AppSettings = AppSettings()):
        super().__init__(app)
        self.app_settings = app_settings
        self.repository = RequestsRepository(app_settings=app_settings)

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)
        try:
            json_body = await request.json()
        except:
            json_body = {}
        response = await call_next(request)
        await self.export_request(request, response, json_body)
        return response

    async def export_request(self, request: Request, response: Response, json_body: dict):
        formatted_request = await DataExporter.format_request(request, json_body)
        formatted_response = await DataExporter.format_response(response)
        result = {
            "request": formatted_request,
            "response": formatted_response,
            "timestamp": datetime.now()
        }
        content_type = "text/html; charset=utf-8"
        if "headers" in result["response"] and "content-type" in result["response"]["headers"]:
            content_type = result["response"]["headers"]["content-type"]
        if content_type != "application/json":
            app_logger.info("Skipping export of request %s", result)
            return
        app_logger.info("Exporting request %s", result)
        try:
            self.repository.add_request(result)
        except Exception as exc:
            app_logger.exception("Error exporting %s", result)

    @staticmethod
    async def format_request(request: Request, json_body: dict):
        result = {
            "method": request.method,
            "body": json_body,
            "url": request.url.components._asdict()
        }
        client = request.client._asdict()
        result["client"] = client
        headers = {}
        for key, value in request.headers.items():
            headers[key] = value
        result["headers"] = headers
        result["path_params"] = request.path_params
        query_params = {
            "kwargs": request.query_params._dict,
            "args": request.query_params._list,
        }
        result["query_params"] = query_params
        return result

    @staticmethod
    async def format_response(response: Response):
        result = {
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }

        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        decoded_body = response_body[0].decode()

        result["body"] = decoded_body

        return result
