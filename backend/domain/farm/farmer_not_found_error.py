class FarmerNotFoundError(Exception):
    def __init__(self):
        self.message = "Farmer not found"
        super().__init__(self.message)
    
    @property
    def get_message(self):
        return self.message