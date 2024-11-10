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


def apply_power_card_effect(card, player, computer):
    """
    Applies the effect of a power card based on its rank.

    Parameters:
    card (Card): The card being played, which has a rank attribute.
    player (Player): The player who played the card.
    computer (Player): The opponent player.

    Returns:
    int: The multiplier for the bet (2 if the card is a King, otherwise 1).

    Effects:
    - If the card is a Jack, the player steals 2 cards from the opponent.
    - If the card is a Queen, the player gains 5 extra chips.
    - If the card is a King, the player's bet for the round is doubled.
    - If the card is an Ace, the player's chips are protected in the next war.
    """
    if card.rank == 'J':
        print(f"{BLUE}Jack's Power:{RESET} Steal 2 cards from the opponent!")
        stolen_cards = draw_cards(computer.deck, 2)
        player.deck.extend(stolen_cards)
        player.cards_won += 2
        computer.cards_won -= 2
    elif card.rank == 'Q':
        print(f"{BLUE}Queen's Power:{RESET} Gain 5 extra chips!")
        player.chips += 5
    elif card.rank == 'K':
        print(f"{BLUE}King's Power:{RESET} Double your bet for this round!")
        return 2
    elif card.rank == 'A':
        print(f"{BLUE}Ace's Power:{RESET} Protect your chips in the next war!")
        player.protected = True
    return 1


def display_welcome_screen():
    print(MAGENTA + """
    ██╗    ██╗ █████╗ ██████╗     ██████╗ █████╗ ██████╗ ██████╗ ███████╗
    ██║    ██║██╔══██╗██╔══██╗   ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    ██║ █╗ ██║███████║██████╔╝   ██║     ███████║██████╔╝██║  ██║███████╗
    ██║███╗██║██╔══██║██╔══██╗   ██║     ██╔══██║██╔══██╗██║  ██║╚════██║
    ╚███╔███╔╝██║  ██║██║  ██║   ╚██████╗██║  ██║██║  ██║██████╔╝███████║
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝
    """ + RESET)

    # Generate 4 random player cards in ASCII art
    deck = create_deck()
    random_cards = random.sample(deck, 4)

    # Print the cards in a horizontal row
    card_lines = [card.ascii_art().splitlines() for card in random_cards]
    for i in range(8):
        # Each card has 7 lines of ASCII art
        # Add 5 spaces to the left for centering
        print("     " + "   ".join(line[i] for line in card_lines))

    print("\n")
    print("Welcome to the Enhanced War Card Game!")
    print("\nMain Menu:")
    print("1. Play Game")
    print("2. See Instructions")
    print("3. See Leaderboards")
    print("4. Tutorial")
    print("5. Quit")


def display_instructions():
    print("\nGame Rules:")
    print(f"1. Each player starts with {INITIAL_CHIPS} chips.")
    print("2. The deck is divided evenly between you and the computer.")
    print("3. Each round, you can bet a number of chips "
          "(minimum 1, maximum based on remaining rounds).")
    print("4. Both players reveal their top card.")
    print("5. The player with the higher card wins the round and the bet.")
    print("6. If there's a tie, a 'war' occurs with increased betting.")
    print("7. Face cards (J, Q, K, A) have special powers when played.")
    print("8. The game ends after the chosen number of rounds, "
          "when a player runs out of cards, or goes bankrupt.")
    print("9. Scoring:")
    print("   - Each card in your possession at the end is worth 10 points.")
    print("   - Each chip you have at the end is worth 1 point.")
    print("10. The player with the highest total score wins the game.")
    print("11. If you go bankrupt, you lose 100 points from your final score.")
    print("12. If you bankrupt the computer, "
          "you gain an additional 100 points.")
    print("13. Leaderboards track highest score, most cards won, "
          "and most chips across all games.")
    input("\nPress Enter to return to the main menu...")


def save_high_score(player):
    high_scores = []
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)

    # Update existing score or add new score
    updated = False
    for score in high_scores:
        if score["name"] == player.name:
            score["highest_score"] = max(score["highest_score"], player.score)
            score["most_cards"] = max(score["most_cards"], player.cards_won)
            score["most_chips"] = max(score["most_chips"], player.chips)
            updated = True
            break

    if not updated:
        high_scores.append({
            "name": player.name,
            "highest_score": player.score,
            "most_cards": player.cards_won,
            "most_chips": player.chips
        })

    high_scores.sort(key=lambda x: x["highest_score"], reverse=True)
    high_scores = high_scores[:10]  # Keep only top 10 scores

    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f)


def display_leaderboards():
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)

        print("\nLeaderboards:")
        print("\nHighest Scores:")
        for i, score in enumerate(
            sorted(
                high_scores, key=lambda x: x
                ["highest_score"], reverse=True)[:5], 1
        ):
            print(f"{i}. {score['name']}: {score['highest_score']} points")

        print("\nMost Cards Won:")
        for i, score in enumerate(
            sorted(
                high_scores, key=lambda x: x["most_cards"], reverse=True)
                [:5], 1
                ):
            print(f"{i}. {score['name']}: {score['most_cards']} cards")

        print("\nMost Chips:")
        for i, score in enumerate(
            sorted(
                high_scores, key=lambda x: x
                ["most_chips"], reverse=True)[:5], 1
        ):
            print(f"{i}. {score['name']}: {score['most_chips']} chips")
    else:
        print("\nNo high scores yet!")
    input("\nPress Enter to return to the main menu...")



print(f"{MAGENTA}Welcome to the game of war cards!{RESET}")
