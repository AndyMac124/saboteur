from typing import Dict, Tuple, Optional
from playing_cards import Names, dirs, DeadEndCard, SpecialCard, BrokenCard, StartCard, GoldCard, GoalCard, TableCard, CrossSectionCard, VerticalPathCard, HorizontalPathCard, TurnLeftCard, TurnRightCard, VertTCard, HorTCard, DEAllCard, DE3ECard, DE3SCard, DEEWCard, DENCard, DENSCard, DEWNCard, DEWSCard, DEWCards
import random

class GameBoard():

    def __init__(self):
        self._board: Dict[Tuple[int, int], Optional[TableCard]] = {(x, y): None for x in range(20) for y in range(20)}

        goal_cards = []
        gold_idx = random.choice([0,1,2])

        self._flippedCards = []

        for i in range(3):
            if gold_idx == i:
                goal_cards.append(GoalCard())
            else:
                goal_cards.append(GoalCard())

        self._board[(6, 10)] = StartCard()
        self.start_point = (6, 10)
        self.goal_locations = [(14,8), (14,10), (14,12)]
        self.gold_loc = self.goal_locations[gold_idx]
        for i, goal in enumerate(goal_cards):
            self._board[self.goal_locations[i]] = goal

    def is_connected_start(self, location):
        seen = set()
        return self.dfs(location, seen)

    def dfs(self, location, seen):
        if location == self.start_point:
            return True

        joins = {
            dirs.NORTH: dirs.SOUTH,
            dirs.SOUTH: dirs.NORTH,
            dirs.EAST: dirs.WEST,
            dirs.WEST: dirs.EAST,
        }

        seen.add(location)
        n, e, s, w = self.get_surrounding(location)

        for next_location in (n, e, s, w):
            if self.is_within_bounds(next_location) and next_location not in seen and self._board[next_location] is not None:
                if type(self._board[next_location]) is not DeadEndCard:
                    next_access = self._board[next_location].get_access_points()
                    cur_access = self._board[location].get_access_points()
                    for n in next_access:
                        if joins[n] in cur_access:
                            if self.dfs(next_location, seen):
                                return True

        return False

    def is_within_bounds(self, location):
        x, y = location
        return 0 <= x < 20 and 0 <= y < 20

    def get_surrounding(self, location):
        x, y = location
        n = (x, y-1)
        e = (x+1, y)
        s = (x, y+1)
        w = (x-1, y)
        return n, e, s, w

    def get_gold_location(self):
        return self.gold_loc

    def get_flipped_cards(self):
        return self._flippedCards

    def get_board(self):
        return self._board

    def copy(self):
        new_board = self._board.copy()
        return new_board

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
            Names.DYNAMITE: BrokenCard(),
        }
        card_class = card_types.get(name.name, None)
        if card_class:
            #print(card_class)
            return card_class
        else:
            print("Card not found")
            return None

    def flip_goal_card(self, loc):
        if loc in self.goal_locations:
            if loc == self.gold_loc:
                self._board[loc] = GoldCard()
            else:
                self._board[loc] = CrossSectionCard()

    def peak_goal_card(self, index):
        if index < 0 or index >= 3:
            return None
        x, y = self._board[self.goal_locations[index]]
        if (x, y) in self.goal_locations:
            if (x, y) is self.gold_loc:
                return True
            else:
                return False
        return None

    # This method does not check if there is a valid path from
    # the starting card to the new placed card
    def add_path_card(self, x, y, card_name):
        #assert isinstance(path_card, PathCard), "The parameter path_card must be an instance of the class PathCard"
        #assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        #assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        #assert self._board.get_item_value(x, y) is None, "There is already another card on the board at coordinates ({0}, {1})".format(x, y)
        if not card_name == Names.DYNAMITE:
            surrounds = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for loc in surrounds:
                if loc in self.goal_locations:
                    self.flip_goal_card(loc)

        self._board[(x, y)] = self.create_card(card_name)

    def add_flipped_path_card(self, x, y, card_name):
        #assert isinstance(path_card, PathCard), "The parameter path_card must be an instance of the class PathCard"
        #assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        #assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        #assert self._board.get_item_value(x, y) is None, "There is already another card on the board at coordinates ({0}, {1})".format(x, y)

        if not card_name == Names.DYNAMITE:
            surrounds = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for loc in surrounds:
                if loc in self.goal_locations:
                    self.flip_goal_card(loc)

        self._flippedCards.append((x, y))
        if (x, y) in self.goal_locations:
            self.flip_goal_card(x, y)
        self._board[(x, y)] = self.create_card(card_name)

    def remove_path_card(self, x, y):
        #assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        #assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        #assert self._board.get_item_value(x, y) is not None and not self._board.get_item_value(x, y).is_special_card(), "There is no valid card to remove at coordinates ({0}, {1})".format(x, y)
        if (x, y) in self._flippedCards:
            self._flippedCards.remove((x, y))

        self._board[(x, y)] = None

    def get_card_image(self, x, y):
        card = self._board.get((x, y))
        if card is not None:
            return card.image
        return None
