class CultureAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "Culture already exists for this farmer"
        super().__init__(self.message)
    
    @property
    def get_message(self):
        return self.args[0]