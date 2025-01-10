from ports.inbound.http.error.http_error import HttpError


class ConflictError(HttpError):
    @property
    def status_code(self) -> int:
        return 409
