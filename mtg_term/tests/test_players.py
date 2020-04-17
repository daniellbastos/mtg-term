import pytest

from mtg_term.constants import INITIAL_LIFE
from mtg_term.exceptions import InvalidPlayerError
from mtg_term.players import Player


@pytest.mark.parametrize('invalid_name', [None, ''])
def test_invalid_empty_name_instance_player(invalid_name):
    with pytest.raises(InvalidPlayerError):
        Player(invalid_name)


def test_valid_instance_player():
    player = Player('foo')

    assert INITIAL_LIFE == player.life
    assert 'foo' == player.name
    assert 'foo' == str(player)
    assert '<Player foo>' == repr(player)
    assert None is player.library
