"""
Prototype for a Wordle-style game. This python script differs from the NYT. Not the same as NYT one, its different.
"""
import random

# Dependencies
target_words_file = "target_words.txt"
all_words_file = "all_words.txt"

# Development mode
# Remove for production
dev_debug = 1
print("\n----- Prototype - Internal Testing - Wordle Game -----\n")
dev_on = input("Enter developer password below (and/or press Enter to continue)\n\n>>> ")

# Game Settings
user_attempts = 1  # Counter for attempts
user_attempts_max = 5  # Max attempts

if dev_on == "password":
    dev_debug = 1
    print("\nDeveloper mode enabled                                                                           DEBUG ON")
    print("                                                                                                 DEBUG ON - User attempt: ", user_attempts)
    print("                                                                                                 DEBUG ON - User attempts max: ", user_attempts_max)
    print("")
else:
    dev_debug = 0
    print("\nNormal Mode enabled\n")

# Read the files
target_file = open(target_words_file,"r")
valid_file = open(all_words_file,"r")

# Context Window with open/close using "with files"
target_data = target_file.read()
valid_data = valid_file.read()

# Split into individual words
target_words = target_data.split()
valid_words = valid_data.split()

# remove whitespace and force lowercase
target_words = [word.strip().lower() for word in target_data.split()]
if dev_debug == True:
    print("                                                                                                 DEBUG ON - Target Words read: ",len(target_words))
valid_words = [word.strip().lower() for word in valid_data.split()]
if dev_debug == 1:
    print("                                                                                                 DEBUG ON - Valid Words read: ",len(valid_words))

# Pick a Target word at random
target_word = random.choice(target_words)
# if dev_debug == 1:
#     print("DEBUG ON - Target Word: ",target_word.upper())


# Function to check the guess against the target word
def score_guess(guess, target_word):
    """
    Compares a guessed word to the target word and returns a score list.

    Scoring:
    - 2 = correct letter in correct position
    - 1 = correct letter in wrong position
    - 0 = letter not in target word
    """
    score = [0] * len(target_word)
    target_list = list(target_word)

    # Check guess against Target Word for correct match and position
    for x in range(len(guess)):
        if guess[x] == target_word[x]:
            score[x] = 2
            target_list[x] = None

    # Check guess against Target Word for correct letter in wrong position
    for x in range(len(guess)):
        if guess[x] != target_word[x]:
            if guess[x] in target_list:
                score[x] = 1
                target_list.remove(guess[x])
            else:
                score[x] = 0
    return score


# Welcome message to User
user_name = input("Hello. We heard you like Word Guessing Games. \nPlease enter your name: ")
print(f"\nWelcome to the Word Guessing Game! I bet you are good at this {user_name}, you have {user_attempts_max} attempts to guess the word.\n")
print("Rules:\n* The word is 5 letters long.\n* English Letters only.\n* No numbers or special characters.\n...if you do, it will still count as a guess!\n")
print("Scoring:\n* 2 = correct letter in correct position\n* 1 = correct letter in wrong position\n* 0 = letter not in target word\n")
print("Settings:\n* Maximum guesses:", user_attempts_max)
print("")

# Loop for User attempts
while user_attempts <= user_attempts_max:
    if dev_debug == 1:
        print("                                                                                             DEBUG ON - Target Word: ",target_word.upper())
        print("\nAttempt", user_attempts, "of", user_attempts_max)
        user_attempts = user_attempts + 1
    else:
        print("\nAttempt", user_attempts, "of", user_attempts_max)
        user_attempts = user_attempts + 1

    # Ask user for a guess
    guess = input("Enter your guess (5-letter word): ")
    guess = guess.lower()

    # Ensure guess is valid
    if len(guess.lower()) != 5 or not all(char in 'abcdefghijklmnopqrstuvwxyz' for char in guess):
        print("Invalid input. Please enter a 5-letter word - You lost a turn!")
        if dev_debug == 1:
            print("                                                                                             DEBUG ON - Invalid User guess: ", guess, "Wrong length or invalid characters")
        continue
    else:
        # Check if guess is in the list of all words
        if guess not in valid_words:
            print("Invalid word. Please enter a read 5-letter word - You lost a turn!")
            if dev_debug == 1:
                print("                                                                                     DEBUG ON - Invalid User guess: ", guess, "not in valid words list")
            continue

    # Set score         #
    scores = score_guess(guess, target_word)
    S1, S2, S3, S4, S5 = scores
    # print(*scores) - only work on 5 characters

    # Output for the user's terminal
    print("\nYour guess is:", guess.upper()) # turn it list list(guess.upper())
    print(guess[0].upper(), guess[1].upper(), guess[2].upper(), guess[3].upper(), guess[4].upper())
    print(S1,S2,S3,S4,S5)
    if dev_debug == 1:
        print(f"                                                                                            DEBUG ON - Score array returned: {scores}")

    # Check if guess is correct
    if guess == target_word:
        print(r"")
        print("\nCongratulations! You guessed the correct word!")
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
        print("\nCongratulations! You guessed the correct word!")
        print("")

        if dev_debug == 1:
             print("                                                                                        DEBUG ON - Guess:", guess.upper(), target_word.upper())
        break

    if guess != target_word and user_attempts <= user_attempts_max:
        print("\nNot the word we are looking for. Try again!")
        if dev_debug == 1:
            print("                                                                                         DEBUG ON - Guess:", guess.upper(), target_word.upper())
            print("                                                                                         DEBUG ON - User : ", user_attempts)
            print("                                                                                         DEBUG ON - User attempts max: ", user_attempts_max)

# User - Game Over
print("                                                                             ")
print("                                                                             ")
print("    ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████  ")
print("   ██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██ ")
print("   ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████  ")
print("   ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██ ")
print("    ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██ ")
print("                                                                             ")
print("                                                                             ")

print("\n\nThat was the last attempt - Game Over! Thanks for playing, ", user_name, "!\n\nThe correct word was:", target_word.upper())
print("\n\n\n")
