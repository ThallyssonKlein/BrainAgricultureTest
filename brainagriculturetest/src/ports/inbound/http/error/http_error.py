from abc import ABC, abstractmethod

class HttpError(ABC):
    def __init__(self, message: str):
        self.message = message

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    def to_dict(self):
        return {
            'status_code': self.status_code,
            'message': self.message
        }