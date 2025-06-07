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

# Function to calculate average attempts
# def show_average_attempts():
#         with open(HISTORY_FILE, "r") as f:
#             lines = f.readlines()
#         attempts = [int(line.strip()) for line in lines if line.strip().isdigit()]
#         if attempts:
#             avg_score = sum(attempts) / len(attempts)
#             print(f"\nAverage number of guesses across games: {avg_score}")

#         return avg_score
def lowest_score():
    history = load_history(HISTORY_FILE)
    lowest_score = float('inf')
    mvp_user = None

    for entry in history:
        if entry.startswith('X-'):
            continue
        score, user = entry.split('=')
        score = int(score)
        user = user.strip().upper()

        if score < lowest_score:
            lowest_score = score
            mvp_user = user

    return lowest_score, mvp_user
# Function to find the MVP user and their lowest score
def find_mvp_user(lowest_score, mvp_user):
    history = load_history(HISTORY_FILE)
    user_scores = {}
    lowest_score = MAX_ATTEMPTS

    for line in history:
        if line.startswith('X-'):
            continue
        else:
            score, user = line.lstrip().split('-')
    if score < lowest_score:
        lowest_score= int(score)
        user = mvp_user.strip().upper()


    for entry in history:
        if entry.startswith('X-'):
            continue
        score, user = entry.split('=')
        score = int(score)
        user = user.strip().upper()

        if user not in user_scores or score < user_scores[user]:
            user_scores[user] = score
            # check new winner
            if score < lowest_score:
                lowest_score = score
                mvp_user = user

    return lowest_score, mvp_user

# Function to find Historic data
def history_attempts():
    history_words = load_history(HISTORY_FILE)
    historic_attempts = [word for word in history_words]
    return historic_attempts

def history_fails(historic_attempts):
    history_words = load_history(HISTORY_FILE)
    fails = [word for word in history_words if word.startswith('X-')]
    #historic_wins = history_attempts(history_words, fails, historic_wins=history_wins)
    historic_wins = [word for word in historic_attempts if word not in fails]
    return fails, historic_wins

def history_wins(history_words, fails, historic_wins):
    historic_wins = [word for word in history_words if word not in fails]
    return historic_wins

def average_attempts(history_wins, history_attempts):
    avg_attempts = len(history_attempts) / len(history_wins)
   # print(f"\nAverage Attempts: {avg_attempts}\n")
    return avg_attempts

# Function to play the game
def play_game(dev_debug, user_name, history_fails):  # DEBUG mode - remove for production
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
        historic_attempts = history_attempts()
        fails, historic_wins = history_fails(historic_attempts)
        avg_score = average_attempts(history_wins, history_attempts)
        lowest_score_value, mvp_user = lowest_score()

        if guess == target_word:
            print("\n Congratulations! You guessed the word!\n")
            print(f"Your score is: {attempts} attempts!")
            print(f"Lowest Score is: {lowest_score} attempts by {mvp_user}.\n")
            print(f"Average number of attempts on winning games {avg_score}")
         #   print (f"Top Scorer is {mvp_user} with a score of {lowest_score}.\n")
            save_history(f"{attempts}={user_name.upper()}")  # Save attempts and user name in score sheet
            return  # Exit the game loop if guessed correctly

        # Function to save and append game history
    print(f"\nGame Over! The word was: {target_word.upper()}")
    save_history(f"X-{user_name.upper()}") # Save 'X' for failed attempts in score sheet
  #  print (f"Top Scorer is {mvp_user} with a score of {lowest_score}.\n")
    print(f"Average number of attempts on winning games {avg_score}")

"""
This is the main function of the game.
"""
def main():
    print("\n----- Prototype - Internal Testing - Wordle Game -----\n".rjust(80))
    dev_on = input("DEBUG: Enter developer password (or press Enter to continue): ")
    if dev_on == DEBUG_PASSWORD:
        print("\nDEBUG mode is ON\n")
        dev_debug = True
    else:
        dev_debug = False

    user_name = input("\nPlease enter your name: ")
    show_help()

    while True:
        historic_attempts = history_attempts()
        fails, historic_wins = history_fails(historic_attempts)
        avg_score = average_attempts(historic_wins, historic_attempts)
        lowest_score, mvp_user = find_mvp_user(None, None)
        # historic_attempts = history_attempts()
        # history_fails, historic_wins = history_fails(history_attempts)

        play_game(dev_debug, user_name, history_fails=history_fails)  # DEBUG mode - remove for production

        print(f"Lowest Score is: {lowest_score} attempts by {mvp_user}.\n")
        print("Average number of attempts on winning games: ", {avg_score})

        play_again = input("\nWow! How fun was that?\n\nShall we Play again? (y/n): \n").lower().strip()
        if play_again != 'y':
            print(f"\nThanks for playing, {user_name}!\n\n")
            break

if __name__ == "__main__":
    main()

# EOF
