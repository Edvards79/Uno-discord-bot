import random
from Uno.rules import RULES


class Card:
    """
    A class to represent a uno card
    ...
    Attributes
    ----------
    COLOURS : list of str
        permitted colours in a uno deck
    CARD_DRAW_TWO : str
        string literal for draw two card
    CARD_DRAW_FOUR : str
        string literal for draw four card
    CARD_REVERSE : str
        string literal for reverse card
    CARD_SKIP : str
        string literal for skip card
    CARD_WILD : str
        string literal for wild card
    value : str
        value of the card
    colour : str, None
        colour of the card
    
    Methods
    -------
    playable(card)
        Returns True if other card is playable on top of this card,
        False otherwise
    """

    COLOURS = ["green", "blue", "yellow", "red"]
    CARD_DRAW_TWO = "+2"
    CARD_DRAW_FOUR = "+4"
    CARD_REVERSE = "reverse"
    CARD_SKIP = "skip"
    CARD_WILD = "wild"


    def __init__(self, value, colour):
        """
        Parameters
        ----------
        value : str
            The value of the card
        colour : str, None
            The colour of the card
        """

        self.value = value
        self.colour = colour
        if self.colour: assert self.colour in self.COLOURS, "Wrong colour for a card."
    
    def playable(self, card, color_chosen=None):
        """Returns True if other card is playable on top of this card,
        False otherwise"""

        return (card.value == self.value or
                card.colour == self.colour or
                self.colour is None or
                self.colour == color_chosen)
    
    def __str__(self):
        return f"[{self.colour}, {self.value}]" if self.colour else f"({self.value})"
    
    def __eq__(self, other):
        return self.value == other.value and self.colour == other.colour

class Deck:
    """
    A class to represent a uno deck
    ...
    Attributes
    ----------
    cards : list of str
        cards of the deck
    Methods
    -------
    shuffle()
        Shuffles the card deck
    draw_cards()
        Draws cards from the deck
    """

    def __init__(self):
        self.cards = self._initialise_deck()
        self.shuffle()
    
    def shuffle(self):
        """shuffles the deck of cards"""

        random.shuffle(self.cards)
    
    def draw_cards(self, num):
        """Draws cards from the deck"""
        
        cards = []
        for i in range(num):
            if len(self.cards) == 0:
                self.cards = self._initialise_deck()
                self.shuffle()
            cards.append(self.cards.pop(0))
        return cards

    def _initialise_deck(self):
        cards = []

        for color in Card.COLOURS:
            # Crete numbered cards
            for i in range(10):
                cards.append(Card(str(i), color))
                cards.append(Card(str(i), color))

            # Create +2 cards
            for i in range(2):
                cards.append(Card(Card.CARD_DRAW_TWO, color))

            # Create skip cards
            for i in range(2):
                cards.append(Card(Card.CARD_SKIP, color))

            # Create reverse cards
            for i in range(2):
                cards.append(Card(Card.CARD_REVERSE, color))
            
            # Create wild cards
            cards.append(Card(Card.CARD_WILD, None))

            # Create +4 cards
            cards.append(Card(Card.CARD_DRAW_FOUR, None))
        
        return cards