import pytest

from mtg_term.cards import _validate_color
from mtg_term.cards.base import BaseCard, CostCard
from mtg_term.cards.creatures import CreatureCard
from mtg_term.exceptions import InvalidCardError, InvalidColorError, InvalidCostError
from mtg_term.factories import CreatureCardFactory


@pytest.mark.parametrize('color', ['black', 'blue', 'green', 'incolor', 'red', 'white'])
def test_valid_colors(color):
    assert _validate_color(color)


def test_invalid_color():
    assert not _validate_color('brown')


def test_raise_exception_by_invalid_color():
    with pytest.raises(InvalidColorError):
        _validate_color('brown', raise_exception=True)


@pytest.mark.parametrize('cost_str', ['black:1',
                                      'blue:1',
                                      'green:1',
                                      'incolor:1',
                                      'red:1',
                                      'white:1',
                                      'incolor:1;black:1',
                                      'incolor:x;red:1'
                                      'incolor:0'])
def test_valid_instance_cost_card(cost_str):
    cost_card = CostCard(cost_str)
    assert f'<CostCard {cost_str}>' == repr(cost_card)
    assert cost_str == str(cost_card)


def test_validate_get_sanitized_cost_by_color():
    cost_card = CostCard('incolor:x;red:1')
    assert 'x' == cost_card['incolor']
    assert 1 == cost_card['red']


@pytest.mark.parametrize('cost', ['black:',
                                  'brown:1',
                                  ':1',
                                  'green1',
                                  'incolor:y'])
def test_invalid_cost_str(cost):
    assert not CostCard._validate_cost_str(cost)


def test_raise_exception_by_invalid_instance_cost_card():
    with pytest.raises(InvalidCostError):
        CostCard('black')


def test_is_valid_instance_base_card():
    cost = CostCard('red:1')
    base_card = BaseCard(name='Card name', description='Long text...', cost=cost, colors=['red'])

    assert base_card.is_valid()

    assert f'<BaseCard Card name>' == repr(base_card)
    assert 'Card name (red:1)' == str(base_card)

    assert base_card._id
    assert 'Card name' == base_card.name
    assert 'Long text...' == base_card.description
    assert 'red:1' == str(base_card.cost)
    assert cost == base_card.cost
    assert isinstance(base_card.cost, CostCard)
    assert ['red'] == base_card.colors


def test_invalid_instance_base_card_by_required_fields():
    base_card = BaseCard(name='', description='', cost='', colors=[])
    with pytest.raises(InvalidCardError) as expected_exc:
        base_card.is_valid()

    expected_fields = ['name', 'description', 'cost', 'colors']

    assert len(expected_fields) == len(expected_exc.value.errors.keys())
    for field in expected_fields:
        assert field in expected_exc.value.errors


def test_invalid_instance_base_card_by_cost():
    base_card = BaseCard(name='Card name', description='Long text...', cost='red:1', colors=['red'])
    with pytest.raises(InvalidCardError):
        base_card.is_valid()

    assert 'cost' in base_card.errors


def test_invalid_instance_base_card_by_color():
    cost = CostCard('red:1')
    base_card = BaseCard(name='Card name', description='Long text...', cost=cost, colors=['brown'])
    with pytest.raises(InvalidCardError):
        base_card.is_valid()

    assert 'colors' in base_card.errors


def test_invalid_instance_creature_card_by_required_fields():
    creature_card = CreatureCard(name='', description='', cost='', colors=[], power_toughness='')
    with pytest.raises(InvalidCardError) as expected_exc:
        creature_card.is_valid()

    expected_fields = ['name', 'description', 'cost', 'colors', 'power_toughness']

    assert len(expected_fields) == len(expected_exc.value.errors.keys())
    for field in expected_fields:
        assert field in expected_exc.value.errors


def test_invalid_instance_creature_card_by_color():
    with pytest.raises(InvalidColorError):
        CreatureCardFactory(colors=['brown'])


def test_is_valid_instance_creature_card():
    cost = CostCard('red:1')
    creature_card = CreatureCard(name='Card name', description='Long text...', cost=cost, colors=['red'], power_toughness='1/1')

    assert creature_card.is_valid()

    assert creature_card._id
    assert f'<CreatureCard Card name (red:1)>' == repr(creature_card)
    assert 'Card name - 1/1 (red:1)' == str(creature_card)
    assert 'Card name' == creature_card.name
    assert 'Long text...' == creature_card.description
    assert 'red:1' == str(creature_card.cost)
    assert cost == creature_card.cost
    assert isinstance(creature_card.cost, CostCard)
    assert ['red'] == creature_card.colors
    assert '1/1' == creature_card.power_toughness
    assert None is creature_card.image_uris


def test_validate_power_and_toughness_values_creature_card():
    creature_card = CreatureCardFactory(power_toughness='1/2')

    assert creature_card.is_valid()

    assert 1 == creature_card.power
    assert 2 == creature_card.toughness

    assert 1 == creature_card.current_power
    assert 2 == creature_card.current_toughness

    assert '1/2' == creature_card.power_toughness
    assert '1/2' == creature_card.current_power_toughness


def test_validate_power_and_toughness_x_creature_card():
    creature_card = CreatureCardFactory(power_toughness='*/*')

    assert creature_card.is_valid()

    assert '*' == creature_card.power
    assert '*' == creature_card.toughness

    assert '*' == creature_card.current_power
    assert '*' == creature_card.current_toughness

    assert '*/*' == creature_card.power_toughness
    assert '*/*' == creature_card.current_power_toughness
