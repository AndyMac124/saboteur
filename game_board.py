from typing import Dict, Tuple, Optional
from playing_cards import StartCard, GoldCard, GoalCard, TableCard
import random

class GameBoard():

    def __init__(self):
        self._board: Dict[Tuple[int, int], Optional[TableCard]] = {(x, y): None for x in range(20) for y in range(20)}

        goal_cards = []
        gold_idx = random.choice([0,1,2])
        for i in range(3):
            if gold_idx == i:
                goal_cards.append(GoldCard())
            else:
                goal_cards.append(GoalCard())

        self._board[(6, 10)] = StartCard()
        goal_locations = [(14,8), (14,10), (14,12)]
        for i, goal in enumerate(goal_cards):
            self._board[goal_locations[i]] = goal

    
    def get_board(self):
        return self._board

    def copy(self):
        new_board = self._board.copy()
        return new_board

    # This method does not check if there is a valid path from
    # the starting card to the new placed card
    def add_path_card(self, x, y, card_name):
        #assert isinstance(path_card, PathCard), "The parameter path_card must be an instance of the class PathCard"
        #assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        #assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        #assert self._board.get_item_value(x, y) is None, "There is already another card on the board at coordinates ({0}, {1})".format(x, y)
        self._board[(x, y)] = TableCard(card_name)
    
    def remove_path_card(self, x, y):
        #assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        #assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        #assert self._board.get_item_value(x, y) is not None and not self._board.get_item_value(x, y).is_special_card(), "There is no valid card to remove at coordinates ({0}, {1})".format(x, y)
        self._board[(x, y)] = None

    def get_card_image(self, x, y):
        card = self._board.get((x, y))
        if card is not None:
            return card.image
        return None
