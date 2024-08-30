from playing_cards import TableCard, ActionCard, GoalCard, GoldCard, StartCard, Names
import random

class Deck():
    def __init__(self):
        self._deck = []

        self._initialise_deck()
        self.shuffle()
    
    def _initialise_deck(self):
        for i in range(4):
            self._deck.append(TableCard(Names.VERTICAL_PATH))
        
        for i in range(5):
            self._deck.append(TableCard(Names.VERT_T))
        
        for i in range(5):
            self._deck.append(TableCard(Names.CROSS_SECTION))
        
        for i in range(5):
            self._deck.append(TableCard(Names.HOR_T))

        for i in range(3):
            self._deck.append(TableCard(Names.HORIZONTAL_PATH))
        
        for i in range(4):
            self._deck.append(TableCard(Names.TURN_LEFT))
        
        for i in range(5):
            self._deck.append(TableCard(Names.TURN_RIGHT))

        self._deck.append(TableCard(Names.DE_ALL))
        self._deck.append(TableCard(Names.DE_3_E))
        self._deck.append(TableCard(Names.DE_3_S))
        self._deck.append(TableCard(Names.DE_EW))
        self._deck.append(TableCard(Names.DE_N))
        self._deck.append(TableCard(Names.DE_NS))
        self._deck.append(TableCard(Names.DE_WN))
        self._deck.append(TableCard(Names.DE_WS))
        self._deck.append(TableCard(Names.DE_W))

        for i in range(6):
            self._deck.append(ActionCard(Names.MAP))
        
        for i in range(9):
            self._deck.append(ActionCard(Names.SABOTAGE))
        
        for i in range(9):
            self._deck.append(ActionCard(Names.MEND))
        
        for i in range(3):
            self._deck.append(ActionCard(Names.DYNAMITE))

    def shuffle(self):
        random.shuffle(self._deck)

    def draw(self):
        assert len(self._deck) > 0, "There are no more cards in the deck"

        return self._deck.pop()

    def is_empty(self):
        return len(self._deck) == 0