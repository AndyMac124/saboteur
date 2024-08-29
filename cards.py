from abc import abstractmethod
from enum import Enum

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
    DEAD_END = 16

class Card:
    def __init__(self, hidden=True, flipped=False):
        self.hidden = hidden
        self.flipped = flipped
        self.is_special = False
        self.access_points = []

    def face_down(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def getAccessPoints(self):
        return self.access_points

    def rotateCard(self):
        self.flipped = not self.flipped
        access_points = self.getAccessPoints()
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

class GoldCard(Card):
    def __init__(self):
        super().__init__()
        self.is_special = True
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]

class GoalCard(Card):
    def __init__(self):
        super().__init__()
        self.is_special = True
        # Crossroads card
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]

class StartCard(Card):
    def __init__(self):
        super().__init__()
        self.is_special = True
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]

class ActionCard(Card):
    def __init__(self):
        super().__init__()

class MapCard(ActionCard):
    def __init__(self):
        super().__init__()

class SabotageCard(ActionCard):
    def __init__(self):
        super().__init__()

class MendCard(ActionCard):
    def __init__(self):
        super().__init__()

class DynamiteCard(ActionCard):
    def __init__(self):
        super().__init__()

class CrossSection(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST, dirs.WEST]

class VerticalPath(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.NORTH, dirs.SOUTH]

class HorizontalPath(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.EAST, dirs.WEST]

class TurnLeft(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.NORTH, dirs.WEST]

class TurnRight(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.NORTH, dirs.EAST]

class VertT(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.NORTH, dirs.EAST, dirs.WEST]

class HorT(Card):
    def __init__(self):
        super().__init__()
        self.access_points = [dirs.NORTH, dirs.SOUTH, dirs.EAST]

class DeadEnd(Card):
    def __init__(self, access_points):
        super().__init__()
        self.access_points = access_points