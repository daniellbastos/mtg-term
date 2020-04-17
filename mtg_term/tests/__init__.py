from faker import Faker
from faker.providers import BaseProvider

from mtg_term.cards.base import CostCard
from mtg_term.constants import VALID_COLORS


_faker = Faker()


class MTGTermProvider(BaseProvider):
    def color(self):
        return _faker.random_choices(VALID_COLORS)[0]

    def cost_card(self, color=None, cost_card_str=None):
        if cost_card_str:
            return CostCard(cost_card_str)

        if color is None:
            color = _faker.random_choices(VALID_COLORS)[0]

        digit = _faker.random_digit_not_null()
        return CostCard(f'{color}:{digit}')

    def power_toughness(self):
        power = _faker.random_digit_not_null()
        toughness = _faker.random_digit_not_null()
        return f'{power}/{toughness}'


_faker.add_provider(MTGTermProvider)
