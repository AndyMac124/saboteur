from une_ai.models import Agent
from typing import Dict, Tuple, Optional
from playing_cards import TableCard, ActionCard, Names


class SaboteurAgent(Agent):

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)

    def add_all_sensors(self):
        board: Dict[Tuple[int, int], Optional[TableCard]] = {(x, y): None for x in range(20) for y in range(20)}
        self.add_sensor('game-board-sensor', board, lambda m: all(isinstance(opt, TableCard) or opt is None for opt in m.values()))
        self.add_sensor('turn-taking-indicator', 0, lambda n: n in range(0, 8))
        self.add_sensor('cards-in-hand-sensor', [], lambda m: all(isinstance(opt, TableCard) or isinstance(opt, ActionCard) or opt is None for opt in m))
        self.add_sensor('can-mine-sensor', True, lambda v: isinstance(v, bool))

    def add_all_actuators(self):
        self.add_actuator('place-card', ('place', 0, 0, 0),
                          lambda v: isinstance(v, tuple) and v[0] == 'place' and v[1] in range(0, 20)
                                    and isinstance(v[1], int) and v[2] in range(0, 20)
                                    and isinstance(v[2], int) and (isinstance(v[3], int)) and v[3] in range(0, 4))
        self.add_actuator('discard-card', ('discard', 0), lambda v: isinstance(v, tuple) and v[0] == 'discard' and v[1] in range(0, 4))
        self.add_actuator('play-mend-card', False, lambda v: isinstance(v, bool))
        self.add_actuator('play-sabotage-card', False, lambda v: isinstance(v, bool))
        self.add_actuator('play-dynamite-card', False, lambda v: isinstance(v, bool))
        self.add_actuator('play-map-card', False, lambda v: isinstance(v, bool))

    def add_all_actions(self):
        for i in range(0, 20):
            for j in range(0, 20):
                for k in range(0, 4):
                    self.add_action('place-{0}-{1}-{2}'.format(i, j, k),
                            lambda x=i, y=j, c=k: {'place-card': ('place', x, y, c)})
        for i in range(0, 4):
            self.add_action('discard-{0}'.format(i),
                            lambda v=i: {'discard-card': ('discard', v)})
        self.add_action('play-mend-card', lambda: {'play-mend-card': True})
        self.add_action('play-sabotage-card', lambda: {'play-sabotage-card': True})
        self.add_action('play-dynamite-card', lambda: {'play-dynamite-card': True})
        self.add_action('play-map-card', lambda: {'play-map-card': True})
