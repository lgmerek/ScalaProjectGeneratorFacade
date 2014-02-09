

class GeneratorFacadeInitializationError(Exception):
    def __init__(self, message, causedBy):
        self.message = message
        self.causedBy = causedBy
