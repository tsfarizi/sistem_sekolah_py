class DomainException(Exception):
    def __init__(self, detail: str = ""):
        self.detail = detail


class NotFoundException(DomainException):
    pass


class BadRequestException(DomainException):
    pass


class UnauthorizedException(DomainException):
    pass


class ForbiddenException(DomainException):
    pass


class ConflictException(DomainException):
    pass
