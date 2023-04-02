from entities.hello_entities import HelloRequest, HelloResponse


class HelloService:

    def process_talk(self, request: HelloRequest) -> HelloResponse:
        result_msg = f"Olá {request.name}!"
        return HelloResponse(message=result_msg)
