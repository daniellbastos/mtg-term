from mtg_term.cards import _validate_color
from mtg_term.cards.creatures import CreatureCard
from mtg_term.cards.lands import Land
from mtg_term.exceptions import InvalidCreatureError, InvalidLandError, InvalidLibraryError


class Library:
    def __init__(self, colors, lands=[], creatures=[]):
        self.colors = []
        self.creatures = []
        self.lands = []

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

        if creatures:
            self.set_creatures(creatures)

    def validate_lands(self, lands):
        if not all([isinstance(l, Land) for l in lands]):
            raise InvalidLandError('The list of Lands has some invalid Land. Lands {}'.format(lands))

        return True

    def validate_creatures(self, creatures):
        if not all([isinstance(c, CreatureCard) and c.is_valid() for c in creatures]):
            raise InvalidCreatureError('The list of Creatures has some invalid Creature type. Creatures {}'.format(creatures))

        return True

    def set_lands(self, lands):
        self.validate_lands(lands)
        self.lands = sorted(lands)

    def set_creatures(self, creatures):
        self.validate_creatures(creatures)
        self.creatures = creatures

    @property
    def cards(self):
        return self.lands + self.creatures
