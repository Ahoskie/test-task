class BotsBuilderError(Exception):
    """Exception raised for errors in BotsBuilder.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Something went wrong in BotsBuilder"):
        self.message = message
        super().__init__(self.message)
