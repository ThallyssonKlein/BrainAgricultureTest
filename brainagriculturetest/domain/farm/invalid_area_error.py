class InvalidAreaError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    @property
    def get_message(self):
        return self.message