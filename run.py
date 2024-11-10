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

print(f"{MAGENTA}Welcome to the game of war cards!{RESET}")
