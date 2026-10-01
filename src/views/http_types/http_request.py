class HttpRequest:
    def __init__(self, body: dict | None = None, param: dict | None = None) -> None:
        self.body = body
        self.param = param
