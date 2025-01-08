from brainagriculturetest.src.ports.inbound.http.error.http_error import HttpError


class BadRequestError(HttpError):
    @property
    def status_code(self) -> int:
        return 400
