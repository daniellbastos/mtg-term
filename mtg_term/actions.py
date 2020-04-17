from mtg_term.cards.creatures import CreatureCard
from mtg_term.constants import LOSER, WON, NON_DECISION, DIED, LIVED
from mtg_term.exceptions import InvalidCreaturesToCombat, NoDecisionValid


class CombatBetweenCreaturesAction:
    def __init__(self, attacking_creature, attacked_creature):
        self.attacking_creature = attacking_creature
        self.attacked_creature = attacked_creature

    def is_valid(self, raise_exception=True):
        first_validation = all([
            isinstance(self.attacking_creature, CreatureCard),
            isinstance(self.attacked_creature, CreatureCard),
        ])

        if not first_validation:
            raise InvalidCreaturesToCombat('attacking_creature Creature or attacked_creature Creature isn\'t CreatureCard valid')

        second_validation = all([
            self.attacking_creature.is_valid(raise_exception=False),
            self.attacked_creature.is_valid(raise_exception=False)
        ])
        if not second_validation:
            raise InvalidCreaturesToCombat('attacking_creature Creature or attacked_creature Creature isn\'t valid')

        return True

    def fight(self):
        self.is_valid()

        if self.attacking_creature.current_power >= self.attacked_creature.current_toughness:
            return WON

        if self.attacking_creature.current_power < self.attacked_creature.current_toughness:
            return LOSER

        raise NoDecisionValid()


class DecisionCemeteryCombatBetweenCreaturesAction:
    def __init__(self, attacking_creature, attacked_creature):
        self.attacking_creature = attacking_creature
        self.attacked_creature = attacked_creature
        self.attacking_creature_result = NON_DECISION
        self.attacked_creature_result = NON_DECISION

    def run(self):
        attacking_creature_action = CombatBetweenCreaturesAction(self.attacking_creature, self.attacked_creature)
        attacked_creature_action = CombatBetweenCreaturesAction(self.attacked_creature, self.attacking_creature)

        attacking_fight_result = attacking_creature_action.fight()
        attacked_fight_result = attacked_creature_action.fight()

        self.attacking_creature_result = self._decision_lived_or_died(attacking_fight_result, attacked_fight_result)
        self.attacked_creature_result = self._decision_lived_or_died(attacked_fight_result, attacking_fight_result)

    def _decision_lived_or_died(self, attacking_result, attacked_result):
        if attacking_result == LOSER and attacked_result == LOSER:
            return LIVED

        if attacking_result == WON and attacked_result == LOSER:
            return LIVED

        if attacking_result == LOSER and attacked_result == WON:
            return DIED

        if attacking_result == WON and attacked_result == WON:
            return DIED

        raise NoDecisionValid()
