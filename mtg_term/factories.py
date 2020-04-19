from mtg_term.tests import _faker

from mtg_term.cards.base import CostCard
from mtg_term.constants import BLACK, BLUE, GREEN, RED, WHITE
from mtg_term.cards.creatures import CreatureCard
from mtg_term.cards.lands import Mountain, Forest, Island, Swamp, Plains
from mtg_term.libraries import Library


def CreatureCardFactory(**kwargs):
    name = kwargs.get('name', _faker.name())
    description = kwargs.get('description', _faker.text())
    colors = kwargs.get('colors', [_faker.color()])
    cost = kwargs.get('cost', _faker.cost_card(colors[0]))
    power_toughness = kwargs.get('power_toughness', _faker.power_toughness())
    image_uris = kwargs.get('image_uris')

    if isinstance(cost, str):
        cost = CostCard(cost)

    bulk_create = kwargs.get('bulk_create', 1)
    if bulk_create == 1:
        return CreatureCard(name=name, description=description, cost=cost, colors=colors, power_toughness=power_toughness, image_uris=image_uris)

    creature_cards_list = []
    for index in range(0, bulk_create):
        card = CreatureCard(name=name, description=description, cost=cost, colors=colors, power_toughness=power_toughness, image_uris=image_uris)
        creature_cards_list.append(card)

    return creature_cards_list


def LibraryFactory(**kwargs):
    map_color_to_land = {
        GREEN: Forest,
        RED: Mountain,
        BLUE: Island,
        BLACK: Swamp,
        WHITE: Plains,
    }

    colors = kwargs.get('colors', 'red')
    land_data = kwargs.get('land_data', [])
    if not land_data:
        land_data = [{'number': 20, 'color': RED}]

    lands = []
    for ld in land_data:
        cls = map_color_to_land[ld['color']]
        for _ in range(0, ld['number']):
            lands.append(cls())

    bulk_create = kwargs.get('bulk_create', 1)
    if bulk_create == 1:
        return Library(colors, lands)

    libraries_list = []
    for index in range(0, bulk_create):
        libraries_list.append(Library(colors, lands))

    return libraries_list
