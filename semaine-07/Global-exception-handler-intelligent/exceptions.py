class BusinessError(Exception):
    error_code = "BUSINESS_ERROR"
    status_code = 400

    def __init__(
        self,
        message: str,
        details: dict[str, object] | None = None,
    ) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundError(BusinessError):
    error_code = "NOT_FOUND"
    status_code = 404


class ValidationError(BusinessError):
    error_code = "VALIDATION_ERROR"
    status_code = 422


class ConflictError(BusinessError):
    error_code = "CONFLICT"
    status_code = 409