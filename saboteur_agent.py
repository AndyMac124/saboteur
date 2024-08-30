from une_ai.models import Agent
from typing import Dict, Tuple, Optional
from playing_cards import TableCard, ActionCard, Names, GoalCard


class SaboteurAgent(Agent):

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

    def add_all_sensors(self):
        board: Dict[Tuple[int, int], Optional[TableCard]] = {(x, y): None for x in range(20) for y in range(20)}
        self.add_sensor('game-board-sensor', board, lambda m: all(isinstance(opt, TableCard) or isinstance(opt, GoalCard) or opt is None for opt in m.values()))
        self.add_sensor('turn-taking-indicator', 0, lambda n: n in range(0, 8))
        self.add_sensor('cards-in-hand-sensor', [], lambda m: all(isinstance(opt, TableCard) or isinstance(opt, ActionCard) or opt is None for opt in m))
        self.add_sensor('can-mine-sensor', True, lambda v: isinstance(v, bool))
        self.add_sensor('reported-cards-sensor', {}, lambda v: all(isinstance(k, tuple) and len(k) == 2 and all(isinstance(i, int) for i in k) and isinstance(val, bool) for k, val in v.items()))

    def add_all_actuators(self):
        # place, x, y, card
        # discard, *, *, card
        # mend, player, *, card
        # sabotage, player, *, card
        # map, index, *, card
        self.add_actuator('play-card', ('place', 0, 0, 0),
                          lambda v: isinstance(v, tuple) and v[0] in ['place', 'discard', 'mend', 'sabotage', 'map', 'dynamite'] and v[1] in range(0, 20)
                                    and isinstance(v[1], int) and v[2] in range(0, 20)
                                    and isinstance(v[2], int) and (isinstance(v[3], int)) and v[3] in range(0, 4))
        self.add_actuator('rotate-card', False, lambda v: isinstance(v, bool))

    def add_all_actions(self):
        for i in range(0, 20):
            for j in range(0, 20):
                for k in range(0, 4):
                    self.add_action('place-{0}-{1}-{2}'.format(i, j, k),
                            lambda x=i, y=j, c=k: {'play-card': ('place', x, y, c)})
                    self.add_action('dynamite-{0}-{1}-{2}'.format(i, j, k), lambda x=i, y=j, c=k: {'play-card': ('dynamite', x, y, c)})

        self.add_action('rotate-true',
                        lambda: {'rotate-card': True})

        self.add_action('rotate-false',
                        lambda: {'rotate-card': True})

        for i in range(0, 4):
                self.add_action('discard-{0}'.format(i),
                                lambda v=i: {'play-card': ('discard', v)})
        for i in range(0, 8):
            for j in range(0, 4):
                self.add_action('mend-{0}-{1}'.format(i, j), lambda x=i, c=j: {'play-card': ('mend', True, x, c)})
                self.add_action('sabotage-{0}-{1}'.format(i, j), lambda x=i, c=j: {'play-card': ('sabotage', True, x, c)})

        for i in range(0, 3):
            for j in range(0, 4):
                for k in range(0, 2):
                    self.add_action('map-{0}-{1}-{2}'.format(i, k, j), lambda x=i, b=k, c=j: {'play-card': (True, x, b, c)})


