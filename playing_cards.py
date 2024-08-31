from abc import ABC
from enum import Enum
import pygame

class dirs(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

class Names(Enum):
    NONE = 1
    START = 2
    GOAL = 3
    GOLD = 4
    MAP = 5
    SABOTAGE = 6
    MEND = 7
    DYNAMITE = 8
    CROSS_SECTION = 9
    VERTICAL_PATH = 10
    HORIZONTAL_PATH = 11
    TURN_LEFT = 12
    TURN_RIGHT = 13
    VERT_T = 14
    HOR_T = 15
    DE_ALL = 16
    DE_3_E = 17
    DE_3_S = 18
    DE_EW = 19
    DE_N = 20
    DE_NS = 21
    DE_WN = 22
    DE_WS = 23
    DE_W = 24
    BROKEN = 25

class Card(ABC):
    def __init__(self, hidden=False, flipped=False):
        self.hidden = hidden
        self.flipped = flipped
        self.is_special = False
        self.access_points = []

    def __str__(self):
        return f"{self.name}"

    def face_down(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def get_access_points(self):
        return self.access_points

    @staticmethod
    def static_access_points(card_name, flipped=False):
        access_points_map = {
            Names.START: [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST],
            Names.GOAL: [],
            Names.GOLD: [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST],
            Names.CROSS_SECTION: [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST],
            Names.VERTICAL_PATH: [dirs.EAST, dirs.WEST],
            Names.HORIZONTAL_PATH: [dirs.NORTH, dirs.SOUTH],
            Names.TURN_LEFT: [dirs.NORTH, dirs.WEST],
            Names.TURN_RIGHT: [dirs.SOUTH, dirs.WEST],
            Names.VERT_T: [dirs.WEST, dirs.SOUTH, dirs.EAST],
            Names.HOR_T: [dirs.NORTH, dirs.EAST, dirs.SOUTH],
            Names.DE_ALL: [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST],
            Names.DE_3_E: [dirs.NORTH, dirs.EAST, dirs.SOUTH],
            Names.DE_3_S: [dirs.EAST, dirs.SOUTH, dirs.WEST],
            Names.DE_EW: [dirs.EAST, dirs.WEST],
            Names.DE_N: [dirs.NORTH],
            Names.DE_NS: [dirs.NORTH, dirs.SOUTH],
            Names.DE_WN: [dirs.NORTH, dirs.WEST],
            Names.DE_WS: [dirs.SOUTH, dirs.WEST],
            Names.DE_W: [dirs.WEST],
            Names.BROKEN: [],
            Names.DYNAMITE: []
        }

        if flipped:
            access_points_map[Names.TURN_LEFT] = [dirs.SOUTH, dirs.EAST]
            access_points_map[Names.TURN_RIGHT] = [dirs.NORTH, dirs.EAST]
            access_points_map[Names.VERT_T] = [dirs.NORTH, dirs.EAST, dirs.WEST]
            access_points_map[Names.HOR_T] = [dirs.NORTH, dirs.WEST, dirs.SOUTH]
            access_points_map[Names.DE_3_E] = [dirs.NORTH, dirs.WEST, dirs.SOUTH]
            access_points_map[Names.DE_3_S] = [dirs.NORTH, dirs.EAST, dirs.WEST]
            access_points_map[Names.DE_WN] = [dirs.NORTH, dirs.WEST]
            access_points_map[Names.DE_WS] = [dirs.NORTH, dirs.EAST]
            access_points_map[Names.DE_N] = [dirs.SOUTH]
            access_points_map[Names.DE_W] = [dirs.EAST]

        return access_points_map.get(card_name, [])

class ActionCard(Card):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = self.load_action(self.name)

    def load_action(self, name):
        image_paths = {
            Names.GOAL: "images/cards/goal.png",
            Names.MAP: "images/cards/map.png",
            Names.SABOTAGE: "images/cards/sabotage.png",
            Names.MEND: "images/cards/mend.png",
            Names.DYNAMITE: "images/cards/dynamite.png",
        }
        return pygame.image.load(image_paths[self.name]).convert_alpha()

class TableCard(Card):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.image = self.load_image(Names.CROSS_SECTION)

    def load_image(self, name):
        image_paths = {
            Names.START: "images/cards/start.png",
            Names.GOAL: "images/cards/goal.png",
            Names.GOLD: "images/cards/gold.png",
            Names.MAP: "images/cards/map.png",
            Names.SABOTAGE: "images/cards/sabotage.png",
            Names.MEND: "images/cards/mend.png",
            Names.DYNAMITE: "images/cards/dynamite.png",
            Names.CROSS_SECTION: "images/cards/cross_section.png",
            Names.VERTICAL_PATH: "images/cards/vertical_path.png",
            Names.HORIZONTAL_PATH: "images/cards/horizontal_path.png",
            Names.TURN_LEFT: "images/cards/turn_left.png",
            Names.TURN_RIGHT: "images/cards/turn_right.png",
            Names.VERT_T: "images/cards/vert_t.png",
            Names.HOR_T: "images/cards/hor_t.png",
            Names.DE_ALL: "images/cards/de_all.png",
            Names.DE_3_E: "images/cards/de_3_e.png",
            Names.DE_3_S: "images/cards/de_3_s.png",
            Names.DE_EW: "images/cards/de_ew.png",
            Names.DE_N: "images/cards/de_n.png",
            Names.DE_NS: "images/cards/de_ns.png",
            Names.DE_WN: "images/cards/de_wn.png",
            Names.DE_WS: "images/cards/de_ws.png",
            Names.DE_W: "images/cards/de_w.png",
            Names.BROKEN: "images/cards/broken.png",
        }
        return pygame.image.load(image_paths[self.name]).convert_alpha()

    def get_image(self):
        return self.image

class DeadEndCard(TableCard):
    def __init__(self, name):
        super().__init__(name)


class CrossSectionCard(TableCard):
    def __init__(self):
        super().__init__(Names.CROSS_SECTION)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.name = Names.CROSS_SECTION
        self.image = self.load_image(self.name)

class VerticalPathCard(TableCard):
    def __init__(self):
        super().__init__(Names.VERTICAL_PATH)
        self.access_points = [dirs.EAST, dirs.WEST]
        self.name = Names.VERTICAL_PATH
        self.image = self.load_image(self.name)

class HorizontalPathCard(TableCard):
    def __init__(self):
        super().__init__(Names.HORIZONTAL_PATH)
        self.access_points = [dirs.NORTH, dirs.SOUTH]
        self.name = Names.HORIZONTAL_PATH
        self.image = self.load_image(self.name)

class TurnLeftCard(TableCard):
    def __init__(self):
        super().__init__(Names.TURN_LEFT)
        self.access_points = [dirs.NORTH, dirs.WEST]
        self.name = Names.TURN_LEFT
        self.image = self.load_image(self.name)

class TurnRightCard(TableCard):
    def __init__(self):
        super().__init__(Names.TURN_RIGHT)
        self.access_points = [dirs.NORTH, dirs.EAST]
        self.name = Names.TURN_RIGHT
        self.image = self.load_image(self.name)

class VertTCard(TableCard):
    def __init__(self):
        super().__init__(Names.VERT_T)
        self.access_points = [dirs.WEST, dirs.SOUTH, dirs.EAST]
        self.name = Names.VERT_T
        self.image = self.load_image(self.name)

class HorTCard(TableCard):
    def __init__(self):
        super().__init__(Names.HOR_T)
        self.access_points = [dirs.NORTH, dirs.EAST, dirs.SOUTH]
        self.name = Names.HOR_T
        self.image = self.load_image(self.name)

class DEAllCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_ALL)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.name = Names.DE_ALL
        self.image = self.load_image(self.name)

class DE3ECard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_3_E)
        self.access_points = [dirs.NORTH, dirs.EAST, dirs.SOUTH]
        self.name = Names.DE_3_E
        self.image = self.load_image(self.name)

class DE3SCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_3_S)
        self.access_points = [dirs.EAST, dirs.SOUTH, dirs.WEST]
        self.name = Names.DE_3_S
        self.image = self.load_image(self.name)

class DEEWCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_EW)
        self.access_points = [dirs.EAST, dirs.WEST]
        self.name = Names.DE_EW
        self.image = self.load_image(self.name)

class DENCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_N)
        self.access_points = [dirs.NORTH]
        self.name = Names.DE_N
        self.image = self.load_image(self.name)

class DENSCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_NS)
        self.access_points = [dirs.NORTH, dirs.SOUTH]
        self.name = Names.DE_NS
        self.image = self.load_image(self.name)

class DEWNCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_WN)
        self.access_points = [dirs.NORTH, dirs.WEST]
        self.name = Names.DE_WN
        self.image = self.load_image(self.name)

class DEWSCard(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_WS)
        self.access_points = [dirs.SOUTH, dirs.WEST]
        self.name = Names.DE_WS
        self.image = self.load_image(self.name)

class DEWCards(DeadEndCard):
    def __init__(self):
        super().__init__(Names.DE_W)
        self.access_points = [dirs.WEST]
        self.name = Names.DE_W
        self.image = self.load_image(self.name)

class SpecialCard(TableCard):
    def __init__(self, name):
        super().__init__(name)
        self.is_special = True

class StartCard(SpecialCard):
    def __init__(self):
        super().__init__(Names.START)
        self.name = Names.START
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.image = self.load_image(self.name)

class GoalCard(ActionCard):
    def __init__(self):
        super().__init__(Names.GOAL)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.image = pygame.image.load("images/cards/goal.png").convert_alpha()

class GoldCard(SpecialCard):
    def __init__(self):
        super().__init__(Names.GOLD)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.image = self.load_image(Names.GOLD)

class BrokenCard(SpecialCard):
    def __init__(self):
        super().__init__(Names.BROKEN)
        self.access_points = []
        self.image = self.load_image(Names.BROKEN)
