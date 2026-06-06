class NotFoundException(Exception):
    def __init__(self, message: str = "Not found"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(Exception):
    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        super().__init__(self.message)


class ForbiddenException(Exception):
    def __init__(self, message: str = "Forbidden"):
        self.message = message
        super().__init__(self.message)


class BadRequestException(Exception):
    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(self.message)
