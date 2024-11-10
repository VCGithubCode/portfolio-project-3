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


print(f"{MAGENTA}Welcome to the game of war cards!{RESET}")
