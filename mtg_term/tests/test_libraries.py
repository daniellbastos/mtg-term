import pytest

from mtg_term.cards.lands import Forest, Island, Mountain, Plains, Swamp
from mtg_term.exceptions import InvalidColorError, InvalidLandError, InvalidLibraryError, InvalidCreatureError
from mtg_term.libraries import Library
from mtg_term.factories import CreatureCardFactory


@pytest.mark.parametrize('invalid_colors', ['brown', 'red,brown', ''])
def test_invalid_color_instance_library(invalid_colors):
    with pytest.raises(InvalidColorError):
        Library(invalid_colors)


@pytest.mark.parametrize('expected_colors,valid_colors', [
    (['red'], 'red'),
    (['black', 'red'], 'red,black')
])
def test_valid_colors_instance_library(expected_colors, valid_colors):
    library = Library(valid_colors)

    assert expected_colors == library.colors


def test_invalid_type_of_land_instance_library():
    lands = ['land1', Mountain()]

    with pytest.raises(InvalidLandError):
        Library('red', lands=lands)


def test_valid_number_and_type_lands_instance_library():
    lands = [Mountain(), Forest(), Island(), Plains(), Swamp()]

    library = Library('red', lands=lands)

    assert 5 == len(library.lands)


def test_valid_instance_library():
    lands = [Mountain(), Forest()]

    library = Library('red,green', lands=lands)

    assert 'green,red' == str(library)
    assert '<Library green,red>' == repr(library)
    assert 2 == len(library.lands)


def test_append_creatures_to_library():
    lands = [Mountain()]
    creatures = [CreatureCardFactory(color='red')]

    library = Library('red', lands=lands, creatures=creatures)

    assert library.is_valid()
    assert 1 == len(library.lands)
    assert 1 == len(library.creatures)
    assert 2 == len(library.cards)


@pytest.mark.parametrize('field_name,invalid_data', [
    ('lands', None),
    ('lands', ['foo']),
    ('creatures', None),
    ('creatures', ['foo']),
])
def test_override_data_to_update_library_and_made_invalid(field_name, invalid_data):
    lands = [Mountain()]
    creatures = [CreatureCardFactory(color='red')]

    library = Library('red', lands=lands, creatures=creatures)

    setattr(library, field_name, invalid_data)

    assert not library.is_valid()


@pytest.mark.parametrize('expected_exception,field_name,invalid_data', [
    (InvalidLandError, 'lands', None),
    (InvalidLandError, 'lands', ['foo']),
    (InvalidCreatureError, 'creatures', None),
    (InvalidCreatureError, 'creatures', ['foo']),
])
def test_override_data_to_update_library_and_raise_exception(expected_exception, field_name, invalid_data):
    lands = [Mountain()]
    creatures = [CreatureCardFactory(color='red')]

    library = Library('red', lands=lands, creatures=creatures)

    setattr(library, field_name, invalid_data)

    with pytest.raises(expected_exception):
        library.is_valid(raise_exception=True)
