class InvalidCardError(Exception):
    def __init__(self, errors):
        self.errors = errors
        self.message = str(errors)


class InvalidColorError(ValueError):
    pass


class InvalidCostError(ValueError):
    pass


class InvalidCreaturesToCombat(Exception):
    pass


class NoDecisionValid(NotImplementedError):
    pass


class InvalidLandError(Exception):
    pass


class InvalidLibraryError(Exception):
    pass


class InvalidPlayerError(Exception):
    pass
