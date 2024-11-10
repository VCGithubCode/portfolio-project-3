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


def tutorial():
    print("\nWelcome to the War Card Game Tutorial!")

    steps = [
        f"Step 1: Starting the Game\nEach player starts "
        f"with {INITIAL_CHIPS} chips.\n"
        "The deck is shuffled and divided equally between "
        "you and the computer.",
        "Step 2: Card Values\nCards are ranked from lowest to "
        "highest: 2, 3, 4, ..., 10, J, Q, K, A",
        "Step 3: Betting\nBefore each round, you can bet any number of chips "
        "(minimum 1, maximum based on remaining rounds).",
        "Step 4: Playing a Round\nBoth players reveal their top card. "
        "The higher card wins the round and the bet.",
        "Step 5: War\nIf both players reveal cards of the "
        "same rank, a 'war' occurs.\n"
        "The bet is doubled, and each player puts down "
        "3 face-down cards and 1 face-up card.\n"
        "The player with the higher face-up card "
        "wins all the cards played and the increased bet.",
        "Step 6: Power Cards\nFace cards have special powers when played:\n"
        "- Jack: Steal 2 cards from the opponent\n"
        "- Queen: Gain 5 extra chips\n"
        "- King: Double your bet for this round\n"
        "- Ace: Protect your chips in the next war",
        "Step 7: Winning the Game\nThe game ends after "
        "the chosen number of rounds, "
        "when a player runs out of cards, or goes bankrupt.\n"
        "Your final score is calculated as: (cards * 10) + chips\n"
        "Be aware that going bankrupt will deduct "
        "100 points from your score.\n"
        "Bankrupting the computer will reward you with an extra 100 points.\n"
        "You can exit the game by typing 'quit'.\n"
        "The player with the highest total score wins the game.\n"
        "Leaderboards track highest score, most cards "
        "won, and most chips across all games."
    ]

    for step in steps:
        print(f"\n{step}")
        while True:
            user_input = input("Press Enter to continue "
                               "or type 'quit' or 'exit' to return "
                               "to the main menu: ")
            if user_input.lower() == 'quit' or user_input.lower() == 'exit':
                print("Exiting the tutorial...")
                return  # Exit the tutorial
            elif user_input == '':
                break  # Valid input to continue
            else:
                print("Invalid input. Please press Enter to continue "
                      "or type 'quit' to exit.")

    print("\nGood luck and have fun!")
    input("Press Enter to return to the main menu...")


def calculate_max_bet(player_chips, remaining_rounds):
    """Calculate the maximum allowed bet based on
    remaining chips and rounds."""
    return max(MINIMUM_BET, min(
        player_chips // remaining_rounds, player_chips))


def handle_exit(signum, frame):
    """
    Handle the exit signal and perform a graceful shutdown.

    This function is intended to be used as a signal handler for
    interrupt signals (e.g., SIGINT). When the signal is received,
    it prints a message indicating that the game was interrupted
    and then exits the program gracefully.

    Parameters:
    signum (int): The signal number.
    frame (FrameType): The current stack frame (or None).

    Returns:
    None
    """
    print("\nGame interrupted. Exiting gracefully...")
    exit(0)


signal.signal(signal.SIGINT, handle_exit)


def get_user_input(prompt, valid_range=None):
    """
    Prompts the user for input and validates it.

    Args:
        prompt (str): The message displayed to the user.
        valid_range (range, optional): A range of valid integer values.

    Returns:
        str or int: The user's input as a string or integer.
    """
    global accepting_input
    while True:
        if not accepting_input:
            print("Input is currently disabled. Please wait.")
            time.sleep(1)  # Wait for 1 second
            continue

        user_input = input(prompt).lower()
        if user_input in ['quit', 'exit']:
            print("Exiting the game. Thanks for playing!")
            exit(0)
        if valid_range:
            try:
                value = int(user_input)
                if value in valid_range:
                    return value
                print((
                    f"Please enter a number between {valid_range.start} "
                    f"and {valid_range.stop - 1}."
                ))
            except ValueError:
                print("Please enter a valid number.")
        else:
            return user_input


def play_game(player_name):
    """
    Starts and manages the game loop for a card game
    between a player and the computer.

    Args:
        player_name (str): The name of the player.

    The game consists of multiple rounds where the player
    and the computer draw cards from their decks,
    place bets, and compare cards to determine the winner
    of each round. The game continues until one
    of the following conditions is met:
        - The maximum number of rounds is reached.
        - Either the player or the computer runs out of chips.
        - Either the player or the computer runs out of cards.

    The game includes special rules for "war" situations when
    there is a tie, and power card effects
    for certain high-ranking cards (J, Q, K, A).

    At the end of the game, the final scores are calculated based
    on the number of cards and chips
    each player has. The player's score is saved, and the leaderboards
    are displayed.

    Raises:
        ValueError: If the user input for the number of rounds or bet
        is not valid.
    """
    player = Player(player_name)
    computer = Player("Computer")

    while True:
        try:
            max_rounds = get_user_input(
                f"Enter the number of rounds to play "
                f"({MIN_ROUNDS}-{MAX_ROUNDS}): ",
                range(MIN_ROUNDS, MAX_ROUNDS + 1)
            )
            break
        except ValueError:
            print("Please enter a valid number.")

    deck = create_deck()
    random.shuffle(deck)

    player.deck = deck[:26]
    computer.deck = deck[26:]

    rounds_played = 0

    while (
        player.deck
        and computer.deck
        and rounds_played < max_rounds
        and player.chips > 0
        and computer.chips > 0
    ):
        rounds_played += 1
        remaining_rounds = max_rounds - rounds_played + 1
        print(f"\n{YELLOW}Round {rounds_played} of {max_rounds}{RESET}")
        print(f"Your cards: {len(player.deck)} - "
              f"Computer's cards: {len(computer.deck)}")
        print(f"Your chips: {player.chips} - "
              f"Computer's chips: {computer.chips}")

        max_bet = calculate_max_bet(player.chips, remaining_rounds)
        bet = get_user_input(f"Enter your bet ({MINIMUM_BET}-{max_bet}): ",
                             range(MINIMUM_BET, max_bet + 1))

        # Confirm the bet amount
        while True:
            confirm_bet = input(
                f"Are you sure about your bet amount of {bet}? (y/n): "
            ).lower()
            if confirm_bet == 'y':
                break  # Proceed with the game
            elif confirm_bet == 'n':
                print("Please enter a new bet amount.")
                bet = get_user_input(
                    f"Enter your bet ({MINIMUM_BET}-{max_bet}): ",
                    range(MINIMUM_BET, max_bet + 1)
                )
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        get_user_input("Press Enter to play a"
                       " card (or type 'quit' to exit)...")

        player_card = draw_cards(player.deck, 1)[0]
        computer_card = draw_cards(computer.deck, 1)[0]

        print("Your card:")
        print(player_card.ascii_art())
        print("Computer's card:")
        print(computer_card.ascii_art())

        bet_multiplier = 1
        if player_card.rank in ['J', 'Q', 'K', 'A']:
            bet_multiplier = apply_power_card_effect(
                player_card, player, computer)

        result = compare_cards(player_card, computer_card)

        if result == "Player":
            print(f"{GREEN}You win this round!{RESET}\n")
            player.deck.extend([player_card, computer_card])
            player.chips += bet
            player.cards_won += 2
            computer.chips -= bet
        elif result == "Computer":
            print(f"{RED}Computer wins this round!{RESET}\n")
            computer.deck.extend([player_card, computer_card])
            computer.chips += bet
            computer.cards_won += 2
            player.chips -= bet
        else:
            print(f"{YELLOW}It's a tie! Preparing for war...{RESET}\n")
            war_pile = [player_card, computer_card]
            war_bet = min(bet * bet_multiplier, player.chips, computer.chips)
            war_result = war_round(player, computer, war_pile, war_bet)
            if war_result != "Tie":
                print(f"{GREEN if war_result == 'Player' else RED}"
                      f"{war_result} wins the war!{RESET}")

        if player.chips <= 0:
            print(f"{RED}You are bankrupt! You lose 100 more chips!{RESET}")
            player.chips -= 100
            computer.chips += 100
        elif computer.chips <= 0:
            print(f"{GREEN}Computer is bankrupt! "
                  f"You win 100 more chips!{RESET}")
            computer.chips -= 100
            player.chips += 100

    print("\nGame Over!")
    print(f"Your final card count: {len(player.deck)}")
    print(f"Computer's final card count: {len(computer.deck)}")
    print(f"Your final chip count: {player.chips}")
    print(f"Computer's final chip count: {computer.chips}")
    print(f"Total cards won: {player.cards_won}")

    player_score = len(player.deck) * 10 + player.chips
    computer_score = len(computer.deck) * 10 + computer.chips

    player.score = player_score

    print(f"\nYour final score: {player.score}")
    print(f"Computer's final score: {computer_score}")
    print("\nScore Breakdown:")
    print(f"Your cards: {len(player.deck)} x 10 = {len(player.deck) * 10} "
          "points")
    print(f"Your chips: {player.chips} x 1 = {player.chips} points")
    print(f"Total: {player_score} points")

    if player.score > computer_score:
        print(f"\n{GREEN}Congratulations! You win!{RESET}")
    elif player.score < computer_score:
        print(f"\n{RED}Computer wins. Better luck next time!{RESET}")
    else:
        print(f"\n{YELLOW}It's a tie!{RESET}")

    save_high_score(player)
    display_leaderboards()


def main():
    """
    Main function to run the game application.

    This function displays a welcome screen and prompts the user
    to enter a choice from the menu. Based on the user's
    choice, it will either start the game, display instructions,
    show leaderboards, provide a tutorial, or exit the game.

    Choices:
    1. Start the game by entering the player's name.
    2. Display game instructions.
    3. Display the leaderboards.
    4. Show the tutorial.
    5. Exit the game.

    The function runs in a loop until the user chooses to exit.

    Returns:
        None
    """
    while True:
        display_welcome_screen()
        choice = get_user_input("Enter your choice (1-5): ", range(1, 6))

        print("\n")
        print("\n")

        if choice == 1:
            while True:
                player_name = input("Enter your name (or "
                                    "type 'quit' to exit): ")
                if player_name.lower() == 'quit':
                    break  # Exit the loop if the user wants to quit
                if len(player_name) < 1 or len(player_name) > 20:
                    print("Name must be between 1 and 20 characters.")
                    continue  # Prompt again for a valid name
                play_game(player_name)
                break  # Exit the name input loop if valid name is provided
        elif choice == 2:
            display_instructions()
        elif choice == 3:
            display_leaderboards()
        elif choice == 4:
            tutorial()
        elif choice == 5:
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
