"""
Prototype for a Wordle-style game.
"""
import random
import string

TARGET_WORDS_FILE = "target_words.txt"
ALL_WORDS_FILE = "all_words.txt"
HISTORY_FILE = "game_history.txt"
MAX_ATTEMPTS = 5
DEBUG_PASSWORD = "password" # DEBUG mode - remove for production
LETTER_CORRECT = '✔'
LETTER_MISPLACED = '?'
LETTER_INCORRECT = '✖'

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

def print_user_counts():
    history_user_counts = {}
    lines = load_history(HISTORY_FILE)

    for line in lines:
        line = line.strip()
        if len(line) > 2:
            history_user = line[2:]  # Ignore first two characters to get name
            if history_user in history_user_counts:
                history_user_counts[history_user] += 1
            else:
                history_user_counts[history_user] = 1

    print("\n--- User Game Counts:")
    for history_user_counts in history_user_counts:
        print(f"{history_user}: {history_user_counts[history_user]} games")

def count_games():
    with open(HISTORY_FILE, 'r') as f:
        history_lines = [entry.strip() for entry in f.read().split()]
    c_games_played = len(history_lines)
    c_games_failed = 0
    for x_entry in history_lines:
        if x_entry.startswith('X-'):
            c_games_failed += 1
    c_games_won = c_games_played - c_games_failed

    return c_games_played, c_games_won

def user_mvp_game_count():
    with open(HISTORY_FILE, 'r') as f:
        history_lines = [entry.strip() for entry in f.read().split()]

    games_failed = 0
    for line in history_lines:
        if line.startswith("X-"):
            games_failed = games_failed + 1

    games_total = len(history_lines)
    games_won = games_total - games_failed

    return games_total, games_won, games_failed

def rank_summary():
    with open(HISTORY_FILE, 'r') as f:
        history_lines = [entry.strip() for entry in f.read().split()]

    rank_counts = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }

    for line in history_lines:
        if line.startswith("X-"):
            pass
        else:
            first_char = line[0]
            if first_char in rank_counts:
                rank_counts[first_char] += 1

    print("\nWinners Tally:")
    print("1 = Unbelievable! First Guess!! :", rank_counts["1"])
    print("2 = Two guesses? Amazing        :", rank_counts["2"])
    print("3 = You are a thinker!          :", rank_counts["3"])
    print("4 = Great work!                 :", rank_counts["4"])
    print("5 = You made it with 0 left!    :", rank_counts["5"])

def first_lowest_score():
    with open(HISTORY_FILE, 'r') as f:
        history_lines = [line.strip() for line in f.read().split()]

    lowest_score = None
    mvp_user = None

    for line in history_lines:
        if line.startswith("X-"):
            continue

        score_name = line.split("-")
        if len(score_name) == 2:
            score = score_name[0]
            name = score_name[1]

            if lowest_score is None or score < lowest_score:
                lowest_score = score
                mvp_user = name

    return lowest_score, mvp_user

# User Help Function
def show_help():
    print("\nWelcome to the Word Guessing Game!\n")
    print("Rules:")
    print("* The word is 5 letters long.")
    print("* Only English letters: " + string.ascii_letters)
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

# Function to save and append game history
def save_history(attempts):
        with open(HISTORY_FILE, "a+") as f:
            f.write(f"{attempts}\n")

# Function to play the game
def play_game(dev_debug, user_name, games_played, mvp_user, lowest_score):  # DEBUG mode - remove for production
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

        guess = input("Enter your guess: ").lower()

        if len(guess) != 5 or not all(x in string.ascii_letters for x in guess):
            print("Invalid input. Use 5 letters A-Z only. Please try again!")
            continue

        if guess not in valid_words:
            print("Not a valid dictionary word. Please try again!")
            continue

        scores = score_guess(guess, target_word)
        display_score(guess, scores)
        attempts += 1

        if guess == target_word:
            print("\n Congratulations! You guessed the word!\n")
            print(f"Your score is: {attempts} attempts")
            print (f"Top Scorer is {mvp_user} with a score of {lowest_score}.\n")

            save_history(f"{attempts}={user_name.upper()}")  # Save attempts and user name in score sheet
            return

        # Function to save and append game history
    print(f"\nGame Over! The word was: {target_word.upper()}")
    save_history(f"X-{user_name.upper()}") # Save 'X' for failed attempts in score sheet

"""
This is the main function of the game.
"""
def main():
    print("\n----- Prototype - Internal Testing - Wordle Game -----\n".rjust(80))
    dev_on = input("DEBUG: Enter developer password (or press Enter to continue): ".rjust(80)).strip()
    dev_debug = dev_on == DEBUG_PASSWORD

    user_name = input("\nPlease enter your name: ")
    show_help()

    games_played, games_won = count_games()               # << load stats from file
    lowest_score, mvp_user = first_lowest_score()         # << load mvp info from file

    while True:
        play_game(dev_debug, user_name, games_played, mvp_user, lowest_score)

        # Refresh stats after each game
        games_played, games_won = count_games()
        lowest_score, mvp_user = first_lowest_score()

        print(f"\nBest score was: {lowest_score}")
        print(f"First to get it: {mvp_user}")

        play_again = input("\nWow! How fun was that?\n\nShall we Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print(f"\nThanks for playing, {user_name}!\n\n")
            break

# Game loop
if __name__ == "__main__":
    main()

# EOF
