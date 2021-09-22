class Player:
    """
    A class to represent a player
    ...
    Attributes
    ----------
    name : str
        permitted colours in a uno deck
    discord_handle : discord.User
        user's discord handle
    hand : list of Card
        list of player's cards
    has_said_uno : bool
        whether the player has said uno
    
     Methods
    -------
    show_hand()
        Returns a string of player's cards
    can_play(current_card)
        Returns True if player has any playble cards on top of the current card
    """

    def __init__(self, name, discord_handle):
        """
        Parameters
        ----------
        name : str
            name of the player
        discord_handle : discord.User
            user's discord handle
        """

        self.name = name
        self.discord_handle = discord_handle
        self.hand = []
        self.has_said_uno = False
    
    def show_hand(self):
        """Returns a string of player's cards"""

        hand = ""
        for i, card in enumerate(self.hand):
            hand += f"{i}) {card}\n"
        hand += "\n Type the number of the card you want to put down."
        return hand
    
    def can_play(self, current_card):
        """Returns True if player has any playble cards on top of the current card"""

        return any(current_card.playable(card) for card in self.hand)
    
    def say_uno(self):
        """Player says uno"""
        
        self.has_said_uno = True
    
    def __eq__(self, other):
        return self.name == other.name