import pytest

from mtg_term.cards.base import CostCard
from mtg_term.cards.lands import Forest, Island, Mountain, Plains, Swamp
from mtg_term.constants import BLACK, BLUE, GREEN, RED, WHITE
from mtg_term.exceptions import InvalidColorError
from mtg_term.factories import CreatureCardFactory, LibraryFactory


def test_autofill_creature_card_factory():
    creature_card = CreatureCardFactory()

    assert creature_card.name
    assert creature_card.description
    assert creature_card.cost
    assert isinstance(creature_card.cost, CostCard)
    assert creature_card.color
    assert creature_card.power_toughness


def test_bulk_create_creature_card_factory():
    creature_cards_list = CreatureCardFactory(bulk_create=10)

    assert 10 == len(creature_cards_list)


@pytest.mark.parametrize('field_name,custom_value', [
    ('name', 'Custom name'),
    ('description', 'Custom description'),
    ('power_toughness', '5/5'),
])
def test_custom_simple_data_creature_card_factory(field_name, custom_value):
    creature_card = CreatureCardFactory(**{field_name: custom_value})

    assert custom_value == getattr(creature_card, field_name)


@pytest.mark.parametrize('cost_card_value', ['red:1', CostCard('red:1')])
def test_custom_cost_card_data_creature_card_factory(cost_card_value):
    creature_card = CreatureCardFactory(cost=cost_card_value)

    assert str(cost_card_value) == str(creature_card.cost)
    assert isinstance(creature_card.cost, CostCard)


def test_invalid_color_creature_card_factory():
    with pytest.raises(InvalidColorError):
        CreatureCardFactory(color='brown')


def test_valid_library_factory():
    library = LibraryFactory()

    assert 'red' == str(library)
    assert '<Library red>' == repr(library)
    assert 20 == len(library.lands)
    assert isinstance(library.lands[0], Mountain)


def test_valid_simple_custom_library_factory():
    library = LibraryFactory(colors='green', land_data=[{'color': GREEN, 'number': 20}])

    assert 'green' == str(library)
    assert '<Library green>' == repr(library)
    assert 20 == len(library.lands)
    assert isinstance(library.lands[0], Forest)


def test_valid_two_colors_library_factory():
    library = LibraryFactory(colors='red,green', land_data=[{'color': GREEN, 'number': 1}, {'color': RED, 'number': 1}])

    assert 'green,red' == str(library)
    assert '<Library green,red>' == repr(library)
    assert 2 == len(library.lands)
    assert isinstance(library.lands[0], Forest)
    assert isinstance(library.lands[1], Mountain)


def test_valid_all_colors_library_factory():
    library = LibraryFactory(
        colors='red,green,black,blue,white',
        land_data=[{
            'color': GREEN,
            'number': 1
        }, {
            'color': RED,
            'number': 1
        }, {
            'color': BLACK,
            'number': 1
        }, {
            'color': BLUE,
            'number': 1
        }, {
            'color': WHITE,
            'number': 1
        }]
    )

    assert 'black,blue,green,red,white' == str(library)
    assert '<Library black,blue,green,red,white>' == repr(library)
    assert 5 == len(library.lands)
    assert isinstance(library.lands[0], Swamp)
    assert isinstance(library.lands[1], Island)
    assert isinstance(library.lands[2], Forest)
    assert isinstance(library.lands[3], Mountain)
    assert isinstance(library.lands[4], Plains)
