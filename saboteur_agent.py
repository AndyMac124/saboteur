from une_ai.models import Agent, GridMap
from cards import Names

class SaboteurAgent(Agent):

    def __init__(self, agent_program):
        super().__init__("Saboteur Agent", agent_program)

    def add_all_sensors(self):
        self.add_sensor('game-board-sensor', GridMap(20, 20, None),
                        lambda m: all(opt in Names or opt is None for loc in m.get_map() for opt in loc))
        self.add_sensor('turn-taking-indicator', 0, lambda n: n in range(0, 8))
        #cards-in-hand-sensor
        self.add_sensor('can-mine-sensor', True, lambda v: isinstance(v, bool))

    def add_all_actuators(self):
        self.add_actuator('place-card', ('place', 0, 0),
                          lambda v: isinstance(v, tuple) and v[0] == 'place' and v[1] in range(0, 20)
                                    and isinstance(v[1], int) and v[2] in range(0, 20)
                                    and isinstance(v[2], int))
        self.add_actuator('discard-card', ('discard', 0), lambda v: isinstance(v, tuple) and v[0] == 'discard' and v[1] in range(0, 4))
        self.add_actuator('play-mend-card', False, lambda v: isinstance(v, bool))
        self.add_actuator('play-sabotage-card', False, lambda v: isinstance(v, bool))
        self.add_actuator('play-dynamite-card', False, lambda v: isinstance(v, bool))
        self.add_actuator('play-map-card', False, lambda v: isinstance(v, bool))

    def add_all_actions(self):
        for i in range(0, 20):
            for j in range(0, 20):
                self.add_action('place-{0}-{1}'.format(i, j),
                            lambda x=i, y=j: {'place-card': ('place', x, y)})
        for i in range(0, 4):
            self.add_action('discard-{0}'.format(i),
                            lambda v=i: {'discard-card': ('discard', v)})
        self.add_action('play-mend-card', lambda: {'play-mend-card': True})
        self.add_action('play-sabotage-card', lambda: {'play-sabotage-card': True})
        self.add_action('play-dynamite-card', lambda: {'play-dynamite-card': True})
        self.add_action('play-map-card', lambda: {'play-map-card': True})
