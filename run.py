import random
import time
import json
import os
import signal


# Color constants for terminal output
MAGENTA = '\033[35m'
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
WHITE = '\033[37m'


# Game constants
INITIAL_CHIPS = 100
MINIMUM_BET = 1
MIN_ROUNDS = 4
MAX_ROUNDS = 26


# Global variable to track input state
accepting_input = True


class Card:
    """
    A class to represent a playing card.

    Attributes
    ----------
    SUITS : list
        A list of strings representing the four suits of a deck of cards.
    RANKS : list
        A list of strings representing the thirteen ranks of a deck of cards.
    suit : str
        The suit of the card.
    rank : str
        The rank of the card.

    Methods
    -------
    __str__():
        Returns a string representation of the card.
    ascii_art():
        Returns an ASCII art representation of the card.
    """
    """Represents a playing card."""
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, rank):
        """
        Initializes a new instance of the class with the given suit and rank.

        Args:
            suit (str): The suit of the card (
            e.g., 'Hearts', 'Diamonds', 'Clubs', 'Spades').
            rank (str): The rank of the card (
            e.g., '2', '3', '4', ..., '10', 'J', 'Q', 'K', 'A').
        """
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """
        Returns a string representation of the
        object, combining the rank and suit attributes.

        Returns:
            str: A string in the format "{rank}{suit}".
        """
        return f"{self.rank}{self.suit}"

    def ascii_art(self):
        """Returns an ASCII representation of the card."""
        suit_color = RED if self.suit in ['♥', '♦'] else WHITE
        rank_color = WHITE
        space = " " if len(self.rank) == 1 else ""
        return f"""{WHITE}
    +-------+
    |{rank_color}{self.rank}{WHITE}{space}     |
    |       |
    |{suit_color}   {self.suit}   {WHITE}|
    |       |
    |     {space}{rank_color}{self.rank}{WHITE}|
    +-------+"""


class Player:
    """
    A class to represent a player in the game.

    Attributes:
    ----------
    name : str
        The name of the player.
    deck : list
        The deck of cards the player has.
    chips : int
        The number of chips the player has.
    score : int
        The score of the player.
    cards_won : int
        The number of cards the player has won.

    Methods:
    -------
    __init__(name):
        Initializes the player with a name, an empty deck,
        initial chips, a score of 0, and 0 cards won.
    """
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.chips = INITIAL_CHIPS
        self.score = 0
        self.cards_won = 0


def get_card_value(card):
    """
    Returns the value of a card based on its rank.

    Args:
        card (Card): The card object whose value is to be determined.

    Returns:
        int: The index of the card's rank in the Card.RANKS list.
    """
    return Card.RANKS.index(card.rank)


def create_deck():
    return [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]


def draw_cards(deck, num_cards):
    return [deck.pop(0) for _ in range(min(num_cards, len(deck)))]


def war_round(player, computer, war_pile, bet):
    """
    Conducts a round of war in the card game between
    the player and the computer.

    In a war round, each player puts down 3 face-down cards and 1 face-up card.
    The face-up cards are compared to determine the winner of the war round.
    If a player does not have enough cards to continue
    the war, the war is resolved.

    Args:
        player (Player): The player object containing
        the player's deck and chips.
        computer (Player): The computer object
        containing the computer's deck and chips.
        war_pile (list): The pile of cards that are at stake in the war round.
        bet (int): The number of chips being bet on the war round.

    Returns:
        str: The result of the war round, either "Player", "Computer", or
        continues the war.
    """
    if len(player.deck) < 4 or len(computer.deck) < 4:
        return resolve_war(player, computer, war_pile, bet)

    war_pile.extend(draw_cards(player.deck, 3))
    war_pile.extend(draw_cards(computer.deck, 3))
    player_card = draw_cards(player.deck, 1)[0]
    computer_card = draw_cards(computer.deck, 1)[0]
    war_pile.extend([player_card, computer_card])

    print(f"{YELLOW}War!{RESET} Each player puts down 3 face-down "
          "cards and 1 face-up card...")
    time.sleep(1)
    print("Your face-up card for war:")
    print(player_card.ascii_art())
    print("Computer's face-up card for war:")
    print(computer_card.ascii_art())

    result = compare_cards(player_card, computer_card)
    if result == "Player":
        print(f"{GREEN}You win the war!{RESET}\n")
        player.deck.extend(war_pile)
        player.chips += bet
        player.cards_won += len(war_pile)
        computer.chips -= bet
        return "Player"
    elif result == "Computer":
        print(f"{RED}Computer wins the war!{RESET}\n")
        computer.deck.extend(war_pile)
        computer.chips += bet
        computer.cards_won += len(war_pile)
        player.chips -= bet
        return "Computer"
    else:
        print(f"{YELLOW}The war continues! Preparing "
              "for another round of war...{RESET}\n")
        time.sleep(1)
        return war_round(player, computer, war_pile, bet * 2)


def resolve_war(player, computer, war_pile, bet):
    """
    Resolves a war scenario in a card game between the player and the computer.

    Parameters:
    player (Player): The player object containing the
    player's deck, chips, and cards won.
    computer (Player): The computer object containing
    the computer's deck, chips, and cards won.
    war_pile (list): The pile of cards that are at stake in the war.
    bet (int): The number of chips that are being
    bet on the outcome of the war.

    Returns:
    str: The result of the war, either "Player", "Computer", or "Tie".
    """
    if len(player.deck) < len(computer.deck):
        computer.deck.extend(war_pile)
        computer.deck.extend(player.deck)
        player.deck.clear()
        computer.chips += bet
        computer.cards_won += len(war_pile)
        player.chips -= bet
        return "Computer"
    elif len(computer.deck) < len(player.deck):
        player.deck.extend(war_pile)
        player.deck.extend(computer.deck)
        computer.deck.clear()
        player.chips += bet
        player.cards_won += len(war_pile)
        computer.chips -= bet
        return "Player"
    else:
        # In case of a tie with equal cards, split the war pile
        mid = len(war_pile) // 2
        player.deck.extend(war_pile[:mid])
        computer.deck.extend(war_pile[mid:])
        player.cards_won += len(war_pile) // 2
        computer.cards_won += len(war_pile) // 2
        return "Tie"


def compare_cards(player_card, computer_card):
    player_value = get_card_value(player_card)
    computer_value = get_card_value(computer_card)

    if player_value > computer_value:
        return "Player"
    elif player_value < computer_value:
        return "Computer"
    else:
        return "Tie"




print(f"{MAGENTA}Welcome to the game of war cards!{RESET}")
