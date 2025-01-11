from ports.inbound.http.error.http_error import HttpError


class NotFoundError(HttpError):
    @property
    def status_code(self) -> int:
        return 404
