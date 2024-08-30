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

class Card(ABC):
    def __init__(self, hidden=True, flipped=False):
        self.hidden = hidden
        self.flipped = flipped
        self.is_special = False
        self.access_points = []

    def __str__(self):
        return f"Card(name={self.name})"

    def face_down(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def get_access_points(self):
        return self.access_points

    def rotate_card(self):
        self.flipped = not self.flipped
        access_points = self.get_access_points()
        for access in access_points:
            if access == dirs.NORTH:
                self.access_points.append(dirs.SOUTH)
                self.access_points.remove(dirs.NORTH)
            elif access == dirs.EAST:
                self.access_points.append(dirs.WEST)
                self.access_points.remove(dirs.EAST)
            elif access == dirs.SOUTH:
                self.access_points.append(dirs.NORTH)
                self.access_points.remove(dirs.SOUTH)
            elif access == dirs.WEST:
                self.access_points.append(dirs.EAST)
                self.access_points.remove(dirs.WEST)

class ActionCard(Card):
    def __init__(self, name):
        super().__init__()
        self.name = name

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
            Names.DE_W: "images/cards/de_w.png"
        }
        return pygame.image.load(image_paths[self.name]).convert_alpha()

    def get_image(self):
        return self.image

class CrossSectionCard(TableCard):
    def __init__(self):
        super().__init__(Names.CROSS_SECTION)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.name = Names.CROSS_SECTION
        self.image = self.load_image(self.name)

class VerticalPathCard(TableCard):
    def __init__(self):
        super().__init__(Names.VERTICAL_PATH)
        self.access_points = [dirs.NORTH, dirs.SOUTH]
        self.name = Names.VERTICAL_PATH
        self.image = self.load_image(self.name)

class HorizontalPathCard(TableCard):
    def __init__(self):
        super().__init__(Names.HORIZONTAL_PATH)
        self.access_points = [dirs.EAST, dirs.WEST]
        self.name = Names.HORIZONTAL_PATH
        self.image = self.load_image(self.name)

class TurnLeftCard(TableCard):
    def __init__(self):
        super().__init__(Names.TURN_LEFT)
        self.access_points = [dirs.NORTH, dirs.EAST]
        self.name = Names.TURN_LEFT
        self.image = self.load_image(self.name)

class TurnRightCard(TableCard):
    def __init__(self):
        super().__init__(Names.TURN_RIGHT)
        self.access_points = [dirs.NORTH, dirs.WEST]
        self.name = Names.TURN_RIGHT
        self.image = self.load_image(self.name)

class VertTCard(TableCard):
    def __init__(self):
        super().__init__(Names.VERT_T)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST]
        self.name = Names.VERT_T
        self.image = self.load_image(self.name)

class HorTCard(TableCard):
    def __init__(self):
        super().__init__(Names.HOR_T)
        self.access_points = [dirs.NORTH, dirs.EAST, dirs.WEST]
        self.name = Names.HOR_T
        self.image = self.load_image(self.name)

class DEAllCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_ALL)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.name = Names.DE_ALL
        self.image = self.load_image(self.name)

class DE3ECard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_3_E)
        self.access_points = [dirs.NORTH, dirs.EAST, dirs.WEST]
        self.name = Names.DE_3_E
        self.image = self.load_image(self.name)

class DE3SCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_3_S)
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.WEST]
        self.name = Names.DE_3_S
        self.image = self.load_image(self.name)

class DEEWCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_EW)
        self.access_points = [dirs.EAST, dirs.WEST]
        self.name = Names.DE_EW
        self.image = self.load_image(self.name)

class DENCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_N)
        self.access_points = [dirs.NORTH]
        self.name = Names.DE_N
        self.image = self.load_image(self.name)

class DENSCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_NS)
        self.access_points = [dirs.NORTH, dirs.SOUTH]
        self.name = Names.DE_NS
        self.image = self.load_image(self.name)

class DEWNCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_WN)
        self.access_points = [dirs.NORTH, dirs.WEST]
        self.name = Names.DE_WN
        self.image = self.load_image(self.name)

class DEWSCard(TableCard):
    def __init__(self):
        super().__init__(Names.DE_WS)
        self.access_points = [dirs.SOUTH, dirs.WEST]
        self.name = Names.DE_WS
        self.image = self.load_image(self.name)

class DEWCards(TableCard):
    def __init__(self):
        super().__init__(Names.DE_W)
        self.access_points = [dirs.WEST]
        self.name = Names.DE_W
        self.image = self.load_image(self.name)

class StartCard(TableCard):
    def __init__(self):
        super().__init__(Names.START)
        self.is_special = True
        self.name = Names.START
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.image = self.load_image(self.name)

class GoalCard(TableCard):
    def __init__(self):
        super().__init__(Names.GOAL)
        self.is_special = True
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        self.hidden = True
        if self.hidden:
            self.image = self.load_image(self.name)
        else:
            self.image = self.load_image(Names.CROSS_SECTION)

class GoldCard(TableCard):
    def __init__(self):
        super().__init__(Names.GOLD)
        self.is_special = True
        self.hidden = True
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]
        if self.hidden:
            self.image = self.load_image(Names.GOAL)
        else:
            self.image = self.load_image(self.name)
