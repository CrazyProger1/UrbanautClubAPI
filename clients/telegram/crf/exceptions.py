class HTTPResponseError(Exception):
    def __init__(self, status: int, content: dict | None):
        self.status = status
        self.content = content
