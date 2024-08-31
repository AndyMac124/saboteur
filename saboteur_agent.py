from une_ai.models import Agent
from typing import Dict, Tuple, Optional
from playing_cards import TableCard, ActionCard, Names, GoalCard, Card

class SaboteurAgent(Agent):

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

    def add_all_sensors(self):
        board: Dict[Tuple[int, int], Optional[TableCard]] = {(x, y): None for x in range(20) for y in range(20)}
        self.add_sensor('game-board-sensor', board, lambda m: all(isinstance(opt, TableCard) or isinstance(opt, GoalCard) or opt is None for opt in m.values()))
        self.add_sensor('turn-taking-indicator', 0, lambda n: n in range(0, 8))
        self.add_sensor('cards-in-hand-sensor', [], lambda m: all(isinstance(opt, TableCard) or isinstance(opt, ActionCard) or opt is None for opt in m))
        self.add_sensor('can-mine-sensor', [], lambda v: all(isinstance(b, bool) for b in v))
        self.add_sensor('reported-cards-sensor',{}, lambda v: isinstance(v, dict) and all(isinstance(k, int) and isinstance(val, tuple) and len(val) == 2 and (val[0] is None or isinstance(val[0], Card)) and isinstance(val[1], bool) for k, val in v.items()))
        self.add_sensor('cards-played-sensor', {}, lambda v: all(isinstance(k, int) and isinstance(v[k], list) and all(isinstance(c, Names) for c in v[k]) for k in v))
        self.add_sensor('deck-status', False, lambda v: isinstance(v, bool))
        self.add_sensor('flipped-cards-sensor', [], lambda v: all(isinstance(c, tuple) for c in v))
        self.add_sensor('known-cards-sensor', [[None, None, None] for _ in range(8)], lambda v: isinstance(v, list) and len(v) == 8 and all(isinstance(c, list) and len(c) == 3 and all(isinstance(i, (bool, type(None))) for i in c) for c in v))

    def add_all_actuators(self):
        # place, x, y, card
        # discard, *, *, card
        # mend, player, *, card
        # sabotage, player, *, card
        # map, index, *, card
        self.add_actuator('play-card', ('place', 0, 0, 0),
                          lambda v: isinstance(v, tuple) and v[0] in ['place', 'discard', 'mend', 'sabotage', 'map', 'dynamite', 'rotate', 'pass'] and v[1] in range(0, 20)
                                    and isinstance(v[1], int) and v[2] in range(0, 20)
                                    and isinstance(v[2], int) and (isinstance(v[3], int)) and v[3] in range(0, 4))

    def add_all_actions(self):
        for i in range(0, 20):
            for j in range(0, 20):
                for k in range(0, 4):
                    self.add_action('place-{0}-{1}-{2}'.format(i, j, k),
                            lambda x=i, y=j, c=k: {'play-card': ('place', x, y, c)})
                    self.add_action('pass-{0}-{1}-{2}'.format(i, j, k),
                                    lambda x=i, y=j, c=k: {'play-card': ('pass', x, y, c)})
                    self.add_action('rotate-{0}-{1}-{2}'.format(i, j, k),
                                    lambda x=i, y=j, c=k: {'play-card': ('rotate', x, y, c)})
                    self.add_action('dynamite-{0}-{1}-{2}'.format(i, j, k), lambda x=i, y=j, c=k: {'play-card': ('dynamite', x, y, c)})

        #self.add_action('rotate-true',
                        #lambda: {'rotate-card': True})

        #self.add_action('rotate-false',
                       # lambda: {'rotate-card': True})

        for i in range(0, 4):
                self.add_action('discard-{0}-{1}-{2}'.format(0, 0, i),
                                lambda v=i: {'play-card': ('discard', 0, 0, v)})
        for i in range(0, 8):
            for j in range(0, 4):
                self.add_action('mend-{0}-{1}-{2}'.format(0, i, j), lambda x=i, c=j: {'play-card': ('mend', 0, x, c)})
                self.add_action('sabotage-{0}-{1}-{2}'.format(0, i, j), lambda x=i, c=j: {'play-card': ('sabotage', 0, x, c)})

        for i in range(0, 3):
            for j in range(0, 2):
                for k in range(0, 4):
                    self.add_action('map-{0}-{1}-{2}'.format(i, j, k), lambda x=i, b=j, c=k: {'play-card': ('mend', x, b, c)})


