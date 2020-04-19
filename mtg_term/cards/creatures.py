from mtg_term.cards.base import BaseCard


class CreatureCard(BaseCard):
    _fields = ['name', 'description', 'cost', 'colors', 'power_toughness', 'image_uris']
    _required_fields = ['name', 'description', 'cost', 'colors', 'power_toughness']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_valid(raise_exception=False)

    def __str__(self):
        return f'{self.name} - {self.power_toughness} ({self.cost})'

    def __repr__(self):
        return f'<CreatureCard {self.name} ({self.cost})>'

    def validate_power_toughness(self):
        self._power, self._toughness = self.power_toughness.split('/')
        return True

    @property
    def power(self):
        try:
            return int(self._power)
        except ValueError:
            return self._power

    @property
    def toughness(self):
        try:
            return int(self._toughness)
        except ValueError:
            return self._toughness

    @property
    def current_power(self):
        # TODO implement here all cases to increment or decrement power
        try:
            return int(self._power)
        except ValueError:
            return self._power

    @property
    def current_toughness(self):
        # TODO implement here all cases to increment or decrement toughness
        try:
            return int(self._toughness)
        except ValueError:
            return self._toughness

    @property
    def current_power_toughness(self):
        return f'{self.current_power}/{self.current_toughness}'
