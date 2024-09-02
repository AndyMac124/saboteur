"""
game_board.py
Reference: Heavily modified version of the deck.py file from the starter zip file for this COSC350 assignment.
"""

from typing import Dict, Tuple, Optional
from playing_cards import Card, Names, dirs, DeadEndCard, SpecialCard, StartCard, GoldCard, GoalCard, TableCard, CrossSectionCard, VerticalPathCard, HorizontalPathCard, TurnLeftCard, TurnRightCard, VertTCard, HorTCard, DEAllCard, DE3ECard, DE3SCard, DEEWCard, DENCard, DENSCard, DEWNCard, DEWSCard, DEWCards
import random

GOAL_LOCATIONS = [(14, 8), (14, 10), (14, 12)]

# Class for the game board
class GameBoard():

    def __init__(self):
        # Board is a dictionary of tuples (x, y) to TableCard objects
        self._board: Dict[Tuple[int, int], Optional[TableCard]] = {(x, y): None for x in range(20) for y in range(20)}
        self._board[(6, 10)] = StartCard()
        self.start_point = (6, 10)
        self._flippedCards = []  # For storing which board locations have been rotated 180 degrees
        self.goal_locations = GOAL_LOCATIONS.copy()
        gold_idx = random.choice([0, 1, 2])
        self.gold_loc = self.goal_locations[gold_idx] # Setting gold location for checking later
        # Setting goal cards
        for i in range(3):
            self._board[self.goal_locations[i]] = GoalCard()

    def get_gold_location(self):
        return self.gold_loc  # tuple (x, y)

    def get_flipped_cards(self):
        return self._flippedCards  # list of tuples (x, y)

    def get_board(self):
        return self._board  # dictionary of tuples (x, y) to TableCard objects

    def copy(self):
        new_board = self._board.copy()
        return new_board

    # Used for adding a new card to the board, enum linked to class instantiation
    def create_card(self, name: Names):
        card_types = {
            Names.CROSS_SECTION: CrossSectionCard(),
            Names.VERTICAL_PATH: VerticalPathCard(),
            Names.HORIZONTAL_PATH: HorizontalPathCard(),
            Names.TURN_LEFT: TurnLeftCard(),
            Names.TURN_RIGHT: TurnRightCard(),
            Names.VERT_T: VertTCard(),
            Names.HOR_T: HorTCard(),
            Names.DE_ALL: DEAllCard(),
            Names.DE_3_E: DE3ECard(),
            Names.DE_3_S: DE3SCard(),
            Names.DE_EW: DEEWCard(),
            Names.DE_N: DENCard(),
            Names.DE_NS: DENSCard(),
            Names.DE_WN: DEWNCard(),
            Names.DE_WS: DEWSCard(),
            Names.DE_W: DEWCards(),
        }
        card_class = card_types.get(name.name, None)
        if card_class:
            return card_class
        else:
            print("Card class not found")
            return None

    # Used for flipping a goal card when a path card is placed next to it
    def flip_goal_card(self, loc):
        if loc in self.goal_locations:
            if loc == self.gold_loc:
                self._board[loc] = GoldCard()
            else:
                self._board[loc] = CrossSectionCard()

    # Used for when a player plays map, True if the goal card is the gold card else False
    def peak_goal_card(self, index):
        # Accepts 0, 1, 2 as index from left to right of the goal cards
        assert index in [0, 1, 2], "Index must be 0, 1, or 2 for left to right of the goal cards"
        x, y = self.goal_locations[index]
        if (x, y) == self.gold_loc:
            return True
        else:
            return False

    # Checks if the x, y location we are placing is next to a goal location
    def check_to_flip_goal_card(self, x, y):
        surrounds = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for loc in surrounds:
            if loc in self.goal_locations:
                self.flip_goal_card(loc)

    # Adds a new path card to the board, checking is done in legal actions
    def add_path_card(self, x, y, card_name):
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"

        if not card_name == Names.DYNAMITE:
            self.check_to_flip_goal_card(x, y)
        self._board[(x, y)] = self.create_card(card_name)

    # For adding a path card in a rotated state (180 degrees)
    def add_flipped_path_card(self, x, y, card_name):
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"

        if not card_name == Names.DYNAMITE:
            self.check_to_flip_goal_card(x, y)
        # Need to append this location to flipped cards
        self._flippedCards.append((x, y))
        self._board[(x, y)] = self.create_card(card_name)

    # For removing a path card using dynamite
    def remove_path_card(self, x, y):
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        # If it's in the flipped cards list, remove it
        if (x, y) in self._flippedCards:
            self._flippedCards.remove((x, y))
        self._board[(x, y)] = None
