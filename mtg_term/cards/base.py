import re

from mtg_term.exceptions import InvalidCardError, InvalidCostError
from mtg_term.cards import _validate_color


class CostCard:
    regex_pattern = '([a-z]+):([0-9|x]+)'

    def __init__(self, cost_str):
        """
        cost_str: <str:color>:<int:cost>,<str:color>:<int:cost>,...
        """
        self._validate_cost_str(cost_str, raise_exception=True)
        self._cost_str = cost_str
        self._cost = {color: cost for color, cost in self._cost_list}

    def __str__(self):
        return self._cost_str

    def __repr__(self):
        return f'<CostCard {self._cost_str}>'

    def __getitem__(self, color):
        try:
            return int(self._cost[color])
        except ValueError:
            return self._cost[color]

    @classmethod
    def _validate_cost_str(cls, cost_str, raise_exception=False):
        cls._cost_list = re.findall(cls.regex_pattern, cost_str)
        validated_colors = all([
            _validate_color(c, raise_exception=raise_exception) for c, _ in cls._cost_list
        ])
        validated_cost_str = all([
            validated_colors,
            len(cls._cost_list) > 0,
        ])

        if raise_exception and not validated_cost_str:
            raise InvalidCostError(f'The cost isn\'t valid format. cost: {cost_str}')

        return validated_cost_str


class BaseCard:
    _base_fields = ['name', 'description', 'cost', 'color']
    _base_required_fields = ['name', 'description', 'cost', 'color']
    _fields = []
    _required_fields = []

    def __init__(self, **kwargs):
        self._initialize_fields(**kwargs)

    def __str__(self):
        return f'{self.name} ({self.cost})'

    def __repr__(self):
        return f'<BaseCard {self.name}>'

    def _initialize_fields(self, **kwargs):
        self._all_fields = list(set(self._base_fields + self._fields))
        self._all_required_fields = list(set(self._base_required_fields + self._required_fields))

        for field_name in self._all_fields:
            setattr(self, field_name, kwargs[field_name])

    def is_valid(self, raise_exception=True):
        self._validate_fields()
        if raise_exception and self.errors:
            raise InvalidCardError(self.errors)

        return not bool(self.errors)

    def validate_cost(self):
        if not isinstance(self.cost, CostCard):
            raise TypeError(f'Object of type CostCard has no valid cost. cost: "{self.cost}"')

        return self.cost

    def validate_color(self):
        _validate_color(self.color, raise_exception=True)
        return self.color

    def _validate_fields(self):
        self.errors = {}

        for field_name in self._all_fields:
            fnc_validate_field = getattr(self, f'validate_{field_name}', None)
            if field_name not in self._all_required_fields and fnc_validate_field is None:
                continue

            valid_value_field = bool(getattr(self, field_name))
            if not valid_value_field:
                self.errors[field_name] = ['Empty required field']

            if fnc_validate_field is None:
                continue

            try:
                fnc_validate_field()
            except Exception as exc:
                if field_name in self.errors:
                    self.errors[field_name].append(str(exc))
                else:
                    self.errors[field_name] = [str(exc)]

