
###               ICTPRG302:            AT3 Assessment
###
###               Name:                 Marcus Audino
###               Student Number:       20031458
###               Date:                 06 April 2025
###
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

# Files read with open - context manager
def load_words(filename):
    # (1) Using 'with open' for file reading
    with open(filename, 'r') as f:
        return [word.strip().lower() for word in f.read().split()]

# User Help Function
def show_help():
    print("\nWelcome to the Word Guessing Game!\n")
    print("Rules:")
    print("* The word is 5 letters long.")
    print("* Only English letters (a-z, A-Z).")
    print("* Invalid guesses don't count against your attempts.\n")
    print("Scoring:")
    print("* ✔ = correct letter in correct position")
    print("* ○ = correct letter in wrong position")
    print("* ✖ = letter not in word\n")

# Scoring function
def score_guess(guess, target_word):
    score = [0] * len(target_word)
    target_list = list(target_word)

    for i in range(len(guess)):
        if guess[i] == target_word[i]:
            score[i] = 2
            target_list[i] = None

    for i in range(len(guess)):
        if guess[i] != target_word[i] and guess[i] in target_list:
            score[i] = 1
            target_list[target_list.index(guess[i])] = None

    return score

# User display feature
def display_score(guess, scores):
    guess_chars = list(guess.upper())
    symbols = {2: '✔', 1: '?', 0: '✖'}
    result = [symbols[s] for s in scores]
    print(' '.join(guess_chars))
    print(' '.join(result))
    print()

# Function to save and append game history
def save_history(attempts):
        with open(HISTORY_FILE, "a+") as f:
            f.write(f"{attempts}\n")

# Function to calculate average attempts
def show_average_attempts():
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
        attempts = [int(line.strip()) for line in lines if line.strip().isdigit()]
        if attempts:
            avg = sum(attempts) / len(attempts)
            print(f"\nAverage number of guesses across games: {avg:.2f}")

def play_game(dev_debug):  # DEBUG mode - remove for production
    target_words = load_words(TARGET_WORDS_FILE)
    valid_words = load_words(ALL_WORDS_FILE)

    if dev_debug:  # DEBUG mode - remove for production
        print(f"DEBUG: Loaded {len(target_words)} target words and {len(valid_words)} valid words.".rjust(80))

    target_word = random.choice(target_words)
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        print(f"\nAttempt {attempts + 1} of {MAX_ATTEMPTS}")
        if dev_debug:  # DEBUG mode - remove for production
            print(f"DEBUG: Target word is {target_word.upper()}".rjust(80))

        guess = input("Enter your guess: ").lower()

        if len(guess) != 5 or not all(c in string.ascii_letters for c in guess):
            print("Invalid input. Use 5 letters A-Z only.")
            continue

        if guess not in valid_words:
            print("Not a valid dictionary word.")
            continue

        scores = score_guess(guess, target_word)
        display_score(guess, scores)
        attempts += 1

        if guess == target_word:
            print("\n Congratulations! You guessed the word!\n")
            save_history(attempts)
            return

    print(f"\nGame Over! The word was: {target_word.upper()}")
    save_history(MAX_ATTEMPTS)

def main():
    print("\n----- Prototype - Internal Testing - Wordle Game -----\n".rjust(80))
    dev_on = input("DEBUG: Enter developer password (or press Enter to continue): ".rjust(80)).strip()
    dev_debug = dev_on == DEBUG_PASSWORD  # DEBUG mode - remove for production

    user_name = input("\nPlease enter your name: ")
    show_help()

    while True:
        play_game(dev_debug)  # DEBUG mode - remove for production
        show_average_attempts()

        again = input("\nWow! How fun was that?\n Shall we Play again? (y/n): ").strip().lower()
        if again != 'y':
            print(f"Thanks for playing, {user_name}!")
            break

# Game loop
if __name__ == "__main__":
    main()

# # Development mode - for internal testing only
# dev_debug = False
# print("\n----- Prototype - Internal Testing - Wordle Game -----\n")
# dev_on = input("Enter developer password below (and/or press Enter to continue)\n\n>>> ")

# # Game Settings
# user_attempts = 1  # Counter for attempts
# user_attempts_max = 5  # Max attempts

# if dev_on == "password":
#     dev_debug = 1
#     print("\nDeveloper mode enabled                                                                           DEBUG ON")
#     print("                                                                                                 DEBUG ON - User attempt: ", user_attempts)
#     print("                                                                                                 DEBUG ON - User attempts max: ", user_attempts_max)
#     print("")
# else:
#     dev_debug = 0
#     print("\nNormal Mode enabled\n")

# # Read the files
# target_file = open(target_words_file,"r")
# valid_file = open(all_words_file,"r")

# # Context Window with open/close using "with files"
# target_data = target_file.read()
# valid_data = valid_file.read()

# # Split into individual words
# target_words = target_data.split()
# valid_words = valid_data.split()

# # remove whitespace and force lowercase
# target_words = [word.strip().lower() for word in target_data.split()]
# if dev_debug == True:
#     print("                                                                                                 DEBUG ON - Target Words read: ",len(target_words))
# valid_words = [word.strip().lower() for word in valid_data.split()]
# if dev_debug == 1:
#     print("                                                                                                 DEBUG ON - Valid Words read: ",len(valid_words))

# # Pick a Target word at random
# target_word = random.choice(target_words)
# # if dev_debug == 1:
# #     print("DEBUG ON - Target Word: ",target_word.upper())


# # Function to check the guess against the target word
# def score_guess(guess, target_word):
#     """
#     Compares a guessed word to the target word and returns a score list.

#     Scoring:
#     - 2 = correct letter in correct position
#     - 1 = correct letter in wrong position
#     - 0 = letter not in target word
#     """
#     score = [0] * len(target_word)
#     target_list = list(target_word)

#     # Check guess against Target Word for correct match and position
#     for x in range(len(guess)):
#         if guess[x] == target_word[x]:
#             score[x] = 2
#             target_list[x] = None

#     # Check guess against Target Word for correct letter in wrong position
#     for x in range(len(guess)):
#         if guess[x] != target_word[x]:
#             if guess[x] in target_list:
#                 score[x] = 1
#                 target_list.remove(guess[x])
#             else:
#                 score[x] = 0
#     return score


# # Welcome message to User
# user_name = input("Hello. We heard you like Word Guessing Games. \nPlease enter your name: ")
# print(f"\nWelcome to the Word Guessing Game! I bet you are good at this {user_name}, you have {user_attempts_max} attempts to guess the word.\n")
# print("Rules:\n* The word is 5 letters long.\n* English Letters only.\n* No numbers or special characters.\n...if you do, it will still count as a guess!\n")
# print("Scoring:\n* 2 = correct letter in correct position\n* 1 = correct letter in wrong position\n* 0 = letter not in target word\n")
# print("Settings:\n* Maximum guesses:", user_attempts_max)
# print("")

# # Loop for User attempts
# while user_attempts <= user_attempts_max:
#     if dev_debug == 1:
#         print("                                                                                             DEBUG ON - Target Word: ",target_word.upper())
#         print("\nAttempt", user_attempts, "of", user_attempts_max)
#         user_attempts = user_attempts + 1
#     else:
#         print("\nAttempt", user_attempts, "of", user_attempts_max)
#         user_attempts = user_attempts + 1

#     # Ask user for a guess
#     guess = input("Enter your guess (5-letter word): ")
#     guess = guess.lower()

#     # Ensure guess is valid
#     if len(guess.lower()) != 5 or not all(char in 'abcdefghijklmnopqrstuvwxyz' for char in guess):
#         print("Invalid input. Please enter a 5-letter word - You lost a turn!")
#         if dev_debug == 1:
#             print("                                                                                             DEBUG ON - Invalid User guess: ", guess, "Wrong length or invalid characters")
#         continue
#     else:
#         # Check if guess is in the list of all words
#         if guess not in valid_words:
#             print("Invalid word. Please enter a read 5-letter word - You lost a turn!")
#             if dev_debug == 1:
#                 print("                                                                                     DEBUG ON - Invalid User guess: ", guess, "not in valid words list")
#             continue

#     # Set score         #
#     scores = score_guess(guess, target_word)
#     S1, S2, S3, S4, S5 = scores
#     # print(*scores) - only work on 5 characters

#     # Output for the user's terminal
#     print("\nYour guess is:", guess.upper()) # turn it list list(guess.upper())
#     print(guess[0].upper(), guess[1].upper(), guess[2].upper(), guess[3].upper(), guess[4].upper())
#     print(S1,S2,S3,S4,S5)
#     if dev_debug == 1:
#         print(f"                                                                                            DEBUG ON - Score array returned: {scores}")

#     # Check if guess is correct
#     if guess == target_word:
#         print(r"")
#         print("\nCongratulations! You guessed the correct word!")
#         print(r"")
#         print(r"   __   _____  _   _  __      _____  _  _  ")
#         print(r"   \ \ / / _ \| | | | \ \    / / _ \| \| | ")
#         print(r"    \ V / (_) | |_| |  \ \/\/ / (_) | .` | ")
#         print(r"     |_| \___/ \___/    \_/\_/ \___/|_|\_| ")
#         print(r"                                           ")
#         print(r"")
#         print(r"   __   _____  _   _  __      _____  _  _  ")
#         print(r"   \ \ / / _ \| | | | \ \    / / _ \| \| | ")
#         print(r"    \ V / (_) | |_| |  \ \/\/ / (_) | .` | ")
#         print(r"     |_| \___/ \___/    \_/\_/ \___/|_|\_| ")
#         print(r"                                           ")
#         print(r"")
#         print("\nCongratulations! You guessed the correct word!")
#         print("")

#         if dev_debug == 1:
#              print("                                                                                        DEBUG ON - Guess:", guess.upper(), target_word.upper())
#         break

#     if guess != target_word and user_attempts <= user_attempts_max:
#         print("\nNot the word we are looking for. Try again!")
#         if dev_debug == 1:
#             print("                                                                                         DEBUG ON - Guess:", guess.upper(), target_word.upper())
#             print("                                                                                         DEBUG ON - User : ", user_attempts)
#             print("                                                                                         DEBUG ON - User attempts max: ", user_attempts_max)

# # User - Game Over
# print("                                                                             ")
# print("                                                                             ")
# print("    ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████  ")
# print("   ██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██ ")
# print("   ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████  ")
# print("   ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██ ")
# print("    ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██ ")
# print("                                                                             ")
# print("                                                                             ")

# print("\n\nThat was the last attempt - Game Over! Thanks for playing, ", user_name, "!\n\nThe correct word was:", target_word.upper())
# print("\n\n\n")







# # NUMBER OF TRIES IN A FILE
# # https://realpython.com/python-with-statement/
# # remember in your part b to include code that shows first and last 5 words

# # remove dead code

# # action: python context manager

# # with .... :
# #     https://realpython.com/python-with-statement/
# # Context Managers and Python's with Statement – Real Python
# # In this step-by-step tutorial, you'll learn what the Python with statement is and how to use it with existing context managers. You'll also learn how to create your own context managers.

# # dev_debug use a boolean instead

# # from string import ascii_letters

# # print(*scores)

# # list(guess.upper())

# # put help in a function

# # put reading the words from a file in a function

# # and then structure code such that it starts with declaration

# # only after your definitions are declared, you run the code (either in a main function or the body)

# # User review - use nice characters rather than 0,1,2 (e.g. -, ?, +)

# # invalid guess should not cost a turn

# # Dev - always return 0, 1,2 but have another function that format it like the user asked

# # play again

# # I want to store the number of tries in a file

# # and then if I win say it took 4 tries, on average it takes you 3.5 times

# # <<asked clarifying questions>>
