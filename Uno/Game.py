import random

from Uno.Deck import Deck, Card
from Uno.ReversibleCycle import ReversibleCycle
from Uno.rules import RULES
from Uno.Player import Player


class Game:
    """
    A class to represent a uno game
    ...
    Attributes
    ----------
    players : ReversibleCycle
        list of players in a game
    deck : Deck
        game's deck
    table : list
        list of cards played
    running : bool
        weather game is running
    min_players: int
        min amount of players to start a game
    max_players: int
        max amount of players allowed in a game
    initial_card_count : int
        number of cards given initially to all players
    current_card : Card
        the current card on the top of the table
    colour_chosen : string
        color chosen by a player when wild or +4 card is played
    
    Methods
    -------
    start(card)
        Starts the game
    stop()
        Stops the game
    add_player(player)
        Adds player to the game
    play_card(player, card, color_choice=None)
        Puts a card on the table
    is_turn(player)
        Checks if it's player's turn
    get_player_by_name(username)
        Gets player object by name
    draw_card(Player)
        Draws a card
    next_turn()
        next turn
    """

    def __init__(self):
        self.playerCycle = ReversibleCycle()
        self.deck = Deck()
        self.table = []
        self.running = False
        self.min_players = RULES["MIN_PLAYERS"]["value"]
        self.max_players = RULES["MAX_PLAYERS"]["value"]
        self.initial_card_count = RULES["INITIAL_CARDS"]["value"]
        self.colour_chosen = None

    def start(self):
            """starts the game"""

            # Check for errors
            if self.running: return {"error": "Game is already running!"}
            if len(self.playerCycle.items) < self.min_players: return {"error": "Not enough players!"}
            if len(self.playerCycle.items) >= self.max_players: return {"error": "Game is already full!"}

            self.running = True

            # Deal cards to all players
            for player in self.playerCycle.items:
                player.hand = self.deck.draw_cards(self.initial_card_count)

            random.shuffle(self.playerCycle.items)

            # Put a numbered card on the table
            card = self.deck.draw_cards(1)[0]
            while not card.value.isdigit(): card = self.deck.draw_cards(1)[0]
            self.table.append(card)

            return {"success": "Starting the game... Go to your DMs to play."}
            
    def add_player(self, name, discord_handle):
            """Adds a player to the game"""

            # Check for errors
            player = Player(name, discord_handle)
            if self.running: return {"error": "Game is already in progress."}
            if [p for p in self.playerCycle.items if p == player]: return {"error": "You have already joined the game."}
            if len(self.playerCycle.items) >= self.max_players: return {"error": "Game is already full."}
            
            self.playerCycle.items.append(player)
            return {"success": f"Player {player.name} joined the game."}

    def draw_card(self, player):
        """Draws a card"""

        if RULES["MUST_PLAY"]["value"] and player.can_play(self.current_card):
            return {"error": "You have a card that you can play."}

        if RULES["AUTOPASS"]["value"]:
            self.next_turn()

        # TODO dont let draw cards multiple times
        player.hand.append(self.deck.draw_cards(1)[0])
        return {"success": f"{player.name} drew a card. It's {self.current_player.name}'s turn."}

    def play_card(self, player, card, color_choice=None):
            """Puts a card on the table"""

            if color_choice: self.colour_chosen = color_choice

            # Check for errors
            if not self.is_turn(player): return {"error": "It's not your turn."}
            if not any(c == card for c in player.hand): return {"error": "You don't have such a card."}
            if (card.value == Card.CARD_DRAW_FOUR or card.value == Card.CARD_WILD) and not color_choice: return {"error": "You have to choose a color."}
            if not card.playable(self.current_card, self.colour_chosen): return {"error": "You can't play this card."}

            # Remove card from player's hand
            for i, player_card in enumerate(player.hand):
                if card == player_card:
                    player.hand.pop(i)
                    break
            
            # Add card to the table
            self.table.append(card)
                
            # Player won but didn't say uno
            if len(player.hand) == 0 and not player.has_said_uno:
                to_draw = RULES["NOT_SAY_UNO_CARDS"]["value"]
                player.hand += self.deck.draw_cards(to_draw)
                self.next_turn()
                return {"error": "You forgot to say uno."}
            
            # Player won and said uno
            if len(player.hand) == 0 and player.has_said_uno:
                self.game = Game()
                return {"success": f"Player {player.name} has won."}

            return self._execute_card(player, card)
    
    def get_player_by_name(self, username):
        """Gets player object by name"""

        for player in self.playerCycle.items:
            if player.name == username:
                return player

    def next_turn(self):
        """Next turn"""
        
        # Clear has_said_uno
        for player in self.playerCycle.items: player.has_said_uno = False

        # Clear _color_chosen if it's not wild card on table anymore
        if not self.current_card.value == Card.CARD_WILD and not self.current_card.value == Card.CARD_DRAW_FOUR:
            print("clearing color chosen")
            self.colour_chosen = None

        return next(self.playerCycle)

    def is_turn(self, player):
        """Returns True if if it's player's turn, False otherwise"""

        return self.current_player == player

    @property
    def current_card(self):
        return self.table[-1]

    @property
    def current_player(self):
        return self.playerCycle.get_current()

    def _execute_card(self, player, card):
            
            if card.value == Card.CARD_DRAW_TWO:
                next_player = self.next_turn()
                next_player.hand += self.deck.draw_cards(2)
                if RULES["DRAW_SKIP"]["value"]: self.next_turn()
            
            elif card.value == Card.CARD_DRAW_FOUR:
                next_player = self.next_turn()
                next_player.hand += self.deck.draw_cards(4)
                if RULES["DRAW_SKIP"]["value"]: self.next_turn()
            
            elif card.value == Card.CARD_WILD:
                self.next_turn()
            
            elif card.value == Card.CARD_REVERSE:
                if len(self.playerCycle.items) == 2:
                    if RULES["REVERSE_SKIP"]["value"] is False:
                        self.next_turn()
                else:
                    self.playerCycle.reverse()
                    self.next_turn()
            
            elif card.value == Card.CARD_SKIP:  
                if len(self.playerCycle.items) == 2:
                    self.next_turn()
                else:              
                    self.next_turn()
                    self.next_turn()
            
            else:
                self.next_turn()

            if self.colour_chosen:
                return {"success": f"{player.name} played a card. It's {self.current_player.name}'s turn. Colour chosen is {self.colour_chosen}."}
            else:
                return {"success": f"{player.name} played a card. It's {self.current_player.name}'s turn."}