from mtg_term.constants import INITIAL_LIFE
from mtg_term.exceptions import InvalidPlayerError, InvalidLibraryError
from mtg_term.libraries import Library


class Player:
    def __init__(self, name, library=None):
        if not name:
            raise InvalidPlayerError('Player "name" is required')

        self.name = name
        self.life = INITIAL_LIFE
        self.library = None

        if library:
            self.set_library(library)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Player {self.name}>'

    def validate_library(self, library):
        if not isinstance(library, Library):
            raise InvalidLibraryError('The Library isn\'t a library type')

        library.is_valid(raise_exception=True)
        return True

    def set_library(self, library):
        self.validate_library(library)
        self.library = library
