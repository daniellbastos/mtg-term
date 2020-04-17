import pytest

from mtg_term.actions import CombatBetweenCreaturesAction, DecisionCemeteryCombatBetweenCreaturesAction
from mtg_term.constants import LOSER, WON, DIED, LIVED
from mtg_term.exceptions import InvalidCreaturesToCombat
from mtg_term.factories import CreatureCardFactory


def test_validate_arguments():
    creature1 = CreatureCardFactory()
    creature2 = CreatureCardFactory()

    action = CombatBetweenCreaturesAction(creature1, creature2)
    assert action.is_valid()


@pytest.mark.parametrize('creature1,creature2', [
    (None, CreatureCardFactory()),
    (CreatureCardFactory(), None),
    (CreatureCardFactory(power_toughness='invalid'), CreatureCardFactory()),
    (CreatureCardFactory(), CreatureCardFactory(power_toughness='invalid')),
])
def test_invalid_creatures_to_combat(creature1, creature2):
    action = CombatBetweenCreaturesAction(creature1, creature2)

    with pytest.raises(InvalidCreaturesToCombat):
        action.is_valid()


@pytest.mark.parametrize('expected_result,attacking_creature,attackied_creature', [
    (WON, CreatureCardFactory(power_toughness='1/1'), CreatureCardFactory(power_toughness='1/1')),
    (LOSER, CreatureCardFactory(power_toughness='1/1'), CreatureCardFactory(power_toughness='2/2')),
    (WON, CreatureCardFactory(power_toughness='2/2'), CreatureCardFactory(power_toughness='1/1')),
])
def test_result_of_fights(expected_result, attacking_creature, attackied_creature):
    action = CombatBetweenCreaturesAction(attacking_creature, attackied_creature)

    assert expected_result == action.fight()


@pytest.mark.parametrize('expected_attacking_result,expected_attacked_result,attacking_creature,attackied_creature', [
    (DIED, DIED, CreatureCardFactory(power_toughness='1/1'), CreatureCardFactory(power_toughness='1/1')),
    (DIED, LIVED, CreatureCardFactory(power_toughness='1/1'), CreatureCardFactory(power_toughness='2/2')),
    (LIVED, DIED, CreatureCardFactory(power_toughness='2/2'), CreatureCardFactory(power_toughness='1/1')),
    (LIVED, LIVED, CreatureCardFactory(power_toughness='1/2'), CreatureCardFactory(power_toughness='1/2')),
])
def test_decision_cemetery_combat_between_creatures(expected_attacking_result, expected_attacked_result, attacking_creature, attackied_creature):  # noqa
    decision = DecisionCemeteryCombatBetweenCreaturesAction(attacking_creature, attackied_creature)
    decision.run()

    assert expected_attacking_result == decision.attacking_creature_result
    assert expected_attacked_result == decision.attacked_creature_result
