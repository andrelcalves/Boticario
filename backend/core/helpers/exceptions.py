class DatabaseError(Exception):
    detail: str

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)


class NotFoundError(Exception):
    detail: str

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)


class NotAuthorizedError(Exception):
    detail: str

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)
