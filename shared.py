"""
shared.py

Purpose: Various components shared amongst files and class without depending
on other imports in this project.
"""

from enum import Enum

DEBUG = False


# Enum for the surrounding directions
class Dirs(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


# Enums for the card names
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


# List of dead end enum names
DECards = [
    Names.DE_ALL,
    Names.DE_W,
    Names.DE_N,
    Names.DE_NS,
    Names.DE_WS,
    Names.DE_WN,
    Names.DE_EW,
    Names.DE_3_S,
    Names.DE_3_E
]

