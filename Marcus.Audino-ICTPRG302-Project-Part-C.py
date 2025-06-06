"""
Prototype for a Wordle-style game. Dedicated to my wife, who loves these types of games.
"""
import random
import string

TARGET_WORDS_FILE = "target_words.txt"
ALL_WORDS_FILE = "all_words.txt"
HISTORY_FILE = "game_history.txt"
MAX_ATTEMPTS = 5
DEBUG_PASSWORD = "password" # DEBUG mode - remove for production
LETTER_CORRECT = '✔'  # Options: 2 ✔ ✓
LETTER_MISPLACED = '▲'  # Options: 1 ▲ • ~
LETTER_INCORRECT = '✖'  # Options: 0 ✖ - ×

# Improving UX UI by 1000%
# Fancy ASCII art for the game name
def print_game_name():
    print(r"")
    print("\n\n")
    print(r"")
    print(r" _       __                  __  ______                          _                  ______")
    print(r"| |     / /____   _____ ____/ / / ____/__  __ ___   _____ _____ (_)____   ____ _  / ____/____ _ ____ ___   ___")
    print(r"| | /| / // __ \ / ___// __  / / / __ / / / // _ \ / ___// ___// // __ \ / __ `/ / / __ / __ `// __ `__ \ / _ \ ")
    print(r"| |/ |/ // /_/ // /   / /_/ / / /_/ // /_/ //  __/(__  )(__  )/ // / / // /_/ / / /_/ // /_/ // / / / / //  __/ ")
    print(r"|__/|__/ \____//_/    \__,_/  \____/ \__,_/ \___//____//____//_//_/ /_/\__, /  \____/ \__,_//_/ /_/ /_/ \___/  ")
    print(r"                                                                       /____/                                ")
    print(r"")
    print("\n\n")

# Fancy ASCII art for Congratulations - in one guess
def print_congrats_one():
    print("\n\n")
    print(r"")
    print("\nGame Over!")
    print(r"")
    print(r"__        _______        __  _")
    print(r"\ \      / / _ \ \      / / | |")
    print(r" \ \ /\ / / | | \ \ /\ / /  | |")
    print(r"  \ V  V /| |_| |\ V  V /   |_|")
    print(r"   \_/\_/  \___/  \_/\_/    (_)")
    print(r"")
    print(r"  ___  _   _ _____    ____ _   _ _____ ____ ____    _")
    print(r" / _ \| \ | | ____|  / ___| | | | ____/ ___/ ___|  | |")
    print(r"| | | |  \| |  _|   | |  _| | | |  _| \___ \___ \  | |")
    print(r"| |_| | |\  | |___  | |_| | |_| | |___ ___) |__) | |_|")
    print(r" \___/|_| \_|_____|  \____|\___/|_____|____/____/  (_)")
    print(r"")
    print(r"    _    __  __    _     ________ _   _  ____   _ _ _")
    print(r"   / \  |  \/  |  / \   |__  /_ _| \ | |/ ___| | | | |")
    print(r"  / _ \ | |\/| | / _ \    / / | ||  \| | |  _  | | | |")
    print(r" / ___ \| |  | |/ ___ \  / /_ | || |\  | |_| | |_|_|_|")
    print(r"/_/   \_\_|  |_/_/   \_\/____|___|_| \_|\____| (_|_|_)")
    print(r"")
    print("\n\n")

# Fancy ASCII art for Congratulations - in two or more guesses
def print_congrats_two():
    print("\n\n")
    print(r"")
    print(r"")
    print(r"   __   _____  _   _  __      _____  _  _  ")
    print(r"   \ \ / / _ \| | | | \ \    / / _ \| \| | ")
    print(r"    \ V / (_) | |_| |  \ \/\/ / (_) | .` | ")
    print(r"     |_| \___/ \___/    \_/\_/ \___/|_|\_| ")
    print(r"                                           ")
    print(r"")
    print(r"   __   _____  _   _  __      _____  _  _  ")
    print(r"   \ \ / / _ \| | | | \ \    / / _ \| \| | ")
    print(r"    \ V / (_) | |_| |  \ \/\/ / (_) | .` | ")
    print(r"     |_| \___/ \___/    \_/\_/ \___/|_|\_| ")
    print(r"                                           ")
    print(r"")
    print("")

def print_last_guess():
    print(r"")
    print(r"")
    print(r" _        _    ____ _____    ____ _   _ _____ ____ ____  ")
    print(r"| |      / \  / ___|_   _|  / ___| | | | ____/ ___/ ___| ")
    print(r"| |     / _ \ \___ \ | |   | |  _| | | |  _| \___ \___ \ ")
    print(r"| |___ / ___ \ ___) || |   | |_| | |_| | |___ ___) |__) |")
    print(r"|_____/_/   \_\____/ |_|    \____|\___/|_____|____/____/ ")
    print(r"")

# Fancy ASCII art for Game over
def print_game_over():
    print("                                                                             ")
    print("                                                                             ")
    print("    ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████  ")
    print("   ██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██ ")
    print("   ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████  ")
    print("   ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██ ")
    print("    ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██ ")
    print("                                                                             ")
    print("                                                                             ")

# Files read with open - context manager - Load target words, all words, history and clean
def load_target_words(TARGET_WORDS_FILE):
    with open(TARGET_WORDS_FILE, 'r') as f:
        return [word.strip().lower() for word in f.read().split()]

def load_all_words(ALL_WORDS_FILE):
    with open(ALL_WORDS_FILE, 'r') as f:
        return [word.strip().lower() for word in f.read().split()]

def load_history(HISTORY_FILE):
    with open(HISTORY_FILE, 'r') as f:
        return [word.strip().lower() for word in f.read().split()]

# User Help Function
def show_help():
    print("\nWelcome to the Word Guessing Game!\n")
    print("Rules:")
    print("* The word is 5 letters long.")
    print(f"* Only English letters: {string.ascii_letters}")
    print("* Invalid guesses don't count against your attempts.\n")
    print("Scoring:")
    print(f"* {LETTER_CORRECT} = correct letter in correct position.")
    print(f"* {LETTER_MISPLACED} = correct letter in wrong position.")
    print(f"* {LETTER_INCORRECT} = letter not in the target word.\n")
    print(f" You have {MAX_ATTEMPTS} attempts to guess the word.\n")

# Scoring function
def score_guess(guess, target_word):
    score = [0] * len(target_word)
    target_list = list(target_word)
    guess = guess.lower()

    for x in range(len(guess)):
        if guess[x] == target_word[x]:
            score[x] = 2
            target_list[x] = None

    for x in range(len(guess)):
        if guess[x] != target_word[x] and guess[x] in target_list:
            score[x] = 1
            target_list[target_list.index(guess[x])] = None

    return score

# User scores display function
def display_score(guess, scores):
    guess_chars = list(guess.upper())
    score_symbols = {
        2: LETTER_CORRECT,
        1: LETTER_MISPLACED,
        0: LETTER_INCORRECT
    }
    result = [score_symbols[s] for s in scores]
    print(' '.join(guess_chars))
    print(' '.join(result))
    print("\n")

# Functions to save and append game history, calculate average attempts.
def save_history(attempts):
        with open(HISTORY_FILE, "a+") as f:
            f.write(f"{attempts}\n")

def history_attempts():
    history_words = load_history(HISTORY_FILE)
    historic_attempts = len(history_words)
    return historic_attempts

def history_fails():
    history_words = load_history(HISTORY_FILE)
    fails = [word for word in history_words if word.startswith('x-')]
    history_count = len(history_words)
    history_wins = history_count - len(fails)
    return history_count, history_wins

def average_attempts(history_attempts, history_wins):
    if history_wins == 0:
        return 0
    return history_attempts / history_wins

# Function to play the game / Game loop
def play_game(dev_debug, user_name, history_wins, historic_attempts):  # DEBUG mode - remove for production
    target_words = load_target_words(TARGET_WORDS_FILE)
    valid_words = load_all_words(ALL_WORDS_FILE)

    if dev_debug:  # DEBUG mode - remove for production
        print(f"DEBUG: Loaded {len(target_words)} target words and {len(valid_words)} valid words.".rjust(80))

    # Game start defaults
    target_word = random.choice(target_words)
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        print(f"\nAttempt {attempts + 1} of {MAX_ATTEMPTS}")

        if dev_debug:  # DEBUG mode - remove for production
            print(f"DEBUG: Target word is {target_word.upper()}".rjust(80))

        if attempts == MAX_ATTEMPTS - 1:
            print_last_guess()
            print(f"\nYou have {MAX_ATTEMPTS - attempts} attempt left, {user_name}!")
            input("[Press Enter to make your FINAL guess...]\n\n")

        guess = input("Enter your guess: ").lower()

        # Guess validation
        if len(guess) != 5:
            print("Invalid input. Use 5 letters - Please try again!")
            continue

        if guess not in string.ascii_letters:
            for g in guess:
                if g not in string.ascii_letters:
                    print(f"Invalid input. Use letters, {string.ascii_letters}, Please try again!")
                    continue

        if guess not in valid_words:
            print("Not a valid dictionary word. Please try again!")
            continue

        # Score validation and calculation
        scores = score_guess(guess, target_word)
        display_score(guess, scores)
        attempts += 1

        avg_score = average_attempts(historic_attempts, history_wins)

        if guess == target_word :
            if attempts == 1:
                print_congrats_one()
                print(f"\nCongratulations, {user_name}! You guessed the word '{target_word.upper()}' in ONE ATTEMPT!\n")
                print("Average number of guesses to Win ", avg_score)

            else:
                print_congrats_two()
                print("\n Congratulations! You guessed the word!\n")
                print(f"Your score is: {attempts} attempts!")
                print("Average number of guesses to Win ", avg_score)

            save_history(f"{attempts}-{user_name.upper()}")  # Save scores and user name in score sheet for future ranking feature
            return

    # Function to save and append game history for failed attempts
    print(f"\nGame Over! The word was: {target_word.upper()}\n")
    print(f"Sorry, {user_name}, you didn't guess the word in {MAX_ATTEMPTS} attempts. Please try again!\n")
    save_history(f"X-{user_name.upper()}") # Save 'X' for failed attempts in score sheet with user name for future ranking feature
    print(f"Average number of guesses to Win: {avg_score}")
    print(f"There have been a total of {historic_attempts} attempts so far!\n")

"""
This is the main function of the game.
"""
def main():
    historic_attempts, history_wins = history_fails()

    print("\n----- Prototype - Internal Testing - Wordle Game -----\n")
    dev_on = input("DEBUG: Enter developer password (or press Enter to continue): ")
    if dev_on == DEBUG_PASSWORD:
        print("\nDEBUG mode is ON\n".rjust(80))
        dev_debug = True
    else:
        dev_debug = False

    print_game_name()
    user_name = input("\nPlease enter your name: ")
    show_help()

    while True:
        historic_attempts, history_wins = history_fails()
        avg_score = average_attempts(historic_attempts, history_wins)

        play_game(dev_debug, user_name, history_wins, historic_attempts)  # DEBUG mode - remove for production

        print_game_over()
        play_again = input(f"\nWow! How fun was that?\n\nShall we Play again, {user_name}? (y/n): \n")
        if play_again != 'y':
            print("Average number of attempts on winning games: ", avg_score)
            print(f"\nThere have been a total of {historic_attempts} attempts so far!\n")
            print(f"\nThanks for playing, {user_name}!\n\n")
            print_game_over()
            print_game_name()
            break

if __name__ == "__main__":
    main()

# EOF
