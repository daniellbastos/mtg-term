from mtg_term.cards import _validate_color
from mtg_term.cards.lands import Land
from mtg_term.constants import MAX_NUMBER_LANDS
from mtg_term.exceptions import InvalidLandError, InvalidLibraryError


class Library:
    def __init__(self, colors, lands=[], creatures=[]):
        self._initialize_data(colors, lands, creatures)

    def __str__(self):
        return ','.join(self.colors)

    def __repr__(self):
        return f'<Library {self}>'

    def _initialize_data(self, colors, lands, creatures):
        colors_list = colors.split(',')
        [_validate_color(c, raise_exception=True) for c in colors_list]

        self.colors = sorted(colors_list)

        if lands:
            self.set_lands(lands)

        self.creatures = creatures

    def validate_lands(self, lands):
        if not all([isinstance(l, Land) for l in lands]):
            raise InvalidLandError('The list of Lands has some invalid Land. Lands {}'.format(lands))

        if len(lands) > MAX_NUMBER_LANDS:
            raise InvalidLibraryError('The max of lands is {}. You have {}'.format(MAX_NUMBER_LANDS, len(lands)))

        return True

    def set_lands(self, lands):
        self.validate_lands(lands)
        self.lands = sorted(lands)
