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
    print(r"")
    print(r" _       __                  __  ______                          _                 ______")
    print(r"| |     / /____   _____ ____/ / / ____/__  __ ___   _____ _____ (_)____   ____ _  / ____/____ _ ____ ___   ___")
    print(r"| | /| / // __ \ / ___// __  / / / __ / / / // _ \ / ___// ___// // __ \ / __ `/ / / __ / __ `// __ `__ \ / _ \ ")
    print(r"| |/ |/ // /_/ // /   / /_/ / / /_/ // /_/ //  __/(__  )(__  )/ // / / // /_/ / / /_/ // /_/ // / / / / //  __/ ")
    print(r"|__/|__/ \____//_/    \__,_/  \____/ \__,_/ \___//____//____//_//_/ /_/\__, /  \____/ \__,_//_/ /_/ /_/ \___/  ")
    print(r"                                                                       /____/                                ")
    print(r"")
    print("\n\n")

# Fancy ASCII art for Congratulations - in one guess
def print_congrats_one():
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

# Fancy ASCII art for the last guess
def print_last_guess():
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
    input("Press Enter to Start\n\n")
    print("Rules:")
    print("* The word is 5 letters long.")
    print(f"* Only English letters: {string.ascii_letters}")
    print("* Invalid guesses don't count against your attempts.\n")
    input("Press Enter to continue...\n\n")
    print("Scoring:")
    print(f"* {LETTER_CORRECT} = correct letter in correct position.")
    print(f"* {LETTER_MISPLACED} = correct letter in wrong position.")
    print(f"* {LETTER_INCORRECT} = letter not in the target word.\n\n")
    print(f"You have {MAX_ATTEMPTS} attempts to guess the word.\n")
    input("Press Enter to start the game...\n\n")

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
   # historic_attempts = 1
    history_words = load_history(HISTORY_FILE)
    historic_attempts = len(history_words)
    return historic_attempts

def history_fails():
    historic_attempts = 0
    history_words = load_history(HISTORY_FILE)
    fails = [word for word in history_words if word.startswith('x-')]
    history_count = len(history_words) + 1
    history_wins = history_count - len(fails)
    avg_score = history_count / history_wins
    avg_score = round(avg_score, 2)
    historic_attempts = len(history_words)
    loss_games = historic_attempts - history_wins
    loss_games = loss_games
    return history_count, history_wins, fails, avg_score, loss_games

#def average_attempts(history_words):
#    avg_score = history_count / history_wins#

#    return total_turns / win_count

#End game statistics function
def end_game_statistics(history_words, history_wins):
    total_games = len(history_words)
    total_losses = total_games - history_wins
    percent_game_won = round((history_wins / total_games) * 100, 2) if total_games > 0 else 0
    total_losses = total_losses + 1
    print(f"\nTotal Games Played: {total_games}")
    print(f"Total Games Won: {history_wins}")
    print(f"Total Games Lost: {total_losses}")
    print(f"Percentage of Games Won: {percent_game_won}%")

def game_report(history_words, history_wins, avg_score, attempts, user_name, history_count, loss_games):
    save_history(f"{attempts}-{user_name.upper()}")
    history_word_count = len(history_words)
    history_count = history_count
    history_word_count = history_word_count + 1
    loss_games = loss_games + 1

   # loss_games = history_count - history_wins  # Calculate losses

   # history_word_count = history_word_count + 1 # Increment total games played by 1 for the current game
    percent_game_won = round(history_wins / history_word_count * 100, 2)  # Calculate percentage of games won
    print(f"Total Games Played: {history_word_count}\nTotal Games Won: {history_wins}\nTotal Games Lost: {loss_games}")
    print(f"Percentage of Games Won: {percent_game_won}% | Average number of guesses those who Win take:", (avg_score))
  #  save_history(f"{attempts}-{user_name.upper()}")

# def end_game_win(history_words, history_wins, avg_score, attempts, user_name):
#     save_history(f"{attempts}-{user_name.upper()}")
#     # Game report
#     history_wins += 1  # Increment wins for the user
#     # Results
#     history_word_count = len(history_words)
#     history_word_count = history_word_count + 1 # Increment total games played by 1 for the current game
#     history_losses = history_word_count - history_wins  # Calculate losses
#     percent_game_won = round(history_wins / history_word_count * 100, 2)  # Calculate percentage of games won
#     print(f"Total Games Played: {history_word_count}\nTotal Games Won: {history_wins}\nTotal Games Lost: {history_losses}")
#     print(f"Percentage of Games Won: {percent_game_won}% | Average number of guesses those who Win take:", round(avg_score * 100, 2))
#   #  save_history(f"{attempts}-{user_name.upper()}")

# def end_game_loss(history_words, history_wins, avg_score, attempts, user_name):
#     save_history(f"{attempts}-{user_name.upper()}")
#     # Results
#     history_word_count = len(history_words)
#     history_word_count = history_word_count + 1 # Increment total games played by 1 for the current game
#     history_losses = history_word_count - history_wins  # Calculate losses
#     percent_game_won = round(history_wins / history_word_count * 100, 2)  # Calculate percentage of games won
#     print(f"Total Games Played: {history_word_count}\nTotal Games Won: {history_wins}\nTotal Games Lost: {history_losses}")
#     print(f"Percentage of Games Won: {percent_game_won}% | Average number of guesses those who Win take:", round(avg_score * 100, 2))
#    # save_history(f"{attempts}-{user_name.upper()}")

# Function to play the game / Game loop
def play_game(dev_debug, user_name, history_wins, avg_score, historic_attempts, history_count, loss_games):  # DEBUG mode - remove for production
    target_words = load_target_words(TARGET_WORDS_FILE)
    valid_words = load_all_words(ALL_WORDS_FILE)
    history_words = load_history(HISTORY_FILE)
    history_count = history_count

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
            input("[Deep Breaths! This is your last attempt coming up.] - Relax, and press ENTER to proceed\n")

        guess = input("Enter your guess: ").lower()

        # Guess validation
        if len(guess) != 5:
            print("Invalid input. Use 5 letters - Please try again!")
            continue

        if all(g in string.ascii_letters for g in guess):
            pass  # Valid characters
        else:
            print(f"Invalid input. Use letters: {string.ascii_letters} only. Please try again!")

        # if guess not in string.ascii_letters:
        #     for g in guess:
        #         if g not in string.ascii_letters:
        #             print(f"Invalid input. Use letters: {string.ascii_letters} only. Please try again!")
        #             break
        #     else:
        #         continue

        #     for g in guess:
        #         if g not in string.ascii_letters:
        #             print("Invalid input. Use letters only.")
        #             break
        #     else:
        #         # Only runs if the loop completes with no break
        #         print("Valid input!")

        if guess not in valid_words:
            print("Not a valid dictionary word. Please try again!")
            continue

        # Score validation and calculation
        scores = score_guess(guess, target_word)
        display_score(guess, scores)
        attempts += 1  #

       # avg_score = avg_score # Calculate average attempts on winning games

        if guess == target_word: # Check if the guess is correct in one guess
          #  history_wins += 1  #
            if attempts == 1:
                print_congrats_one()
                print(f"\nCongratulations, {user_name}! You guessed the word {target_word.upper()} in ONE ATTEMPT!\n")
              #  history_wins += 1
                # # Game report
                #history_wins += 1  # Increment wins for the user
                # # Results
                # history_word_count = len(history_words)
                # history_word_count = history_word_count + 1 # Increment total games played by 1 for the current game
                # history_losses = history_word_count - history_wins  # Calculate losses
                # percent_game_won = round(history_wins / history_word_count * 100, 2)  # Calculate percentage of games won

                # print(f"Total Games Played: {history_word_count}\nTotal Games Won: {history_wins}\nTotal Games Lost: {history_losses}")
                # print(f"Percentage of Games Won: {percent_game_won}% | Average number of guesses those who Win take:", round(avg_score * 100, 2))
                # save_history(f"{attempts}-{user_name.upper()}")
                game_report(history_words, history_wins, avg_score, attempts, user_name, history_count, loss_games)  # Save scores and user name in score sheet for future ranking feature
            else:
                print_congrats_two()  # Check if the guess is correct in two or more guesses
                print(f"Congratulations! {user_name}! You guessed the word {target_word.upper()} in {attempts} attempts!")
               # history_wins += 1
                game_report(history_words, history_wins, avg_score, attempts, user_name, history_count, loss_games) # Save scores and user name in score sheet for future ranking feature


                # Game report
                # Game report
            #    print(f"Total Games Played: {len(history_words)}\nTotal Games Won: {history_wins}\nTotal Games Lost: {len(history_words) - history_wins}\n")
            #    print(f"Percentage of Games Won: {round((history_wins / len(history_words)) * 100, 2)}%")
            #    print(f"Total Games Played: {len(history_words)}")
            #    print("Average number of guesses those who Win take:", (avg_score))
       #         save_history(f"{attempts}-{user_name.upper()}")  # Save scores and user name in score sheet for future ranking feature
            return

    # Function to save and append game history for failed attempts

    # end_stat = len(history_words)
    # end_stat = end_stat + 1 # Increment total games played by 1 for the current game

    print(f"\nGame Over! The word was: {target_word.upper()}\n")
    print(f"Sorry, {user_name}, you didn't guess the word in {MAX_ATTEMPTS} attempts. Please play again!\n")
    save_history(f"X-{user_name.upper()}") # Save 'X' for failed attempts in score sheet with user name for future ranking feature
    game_report(history_words, history_wins, avg_score, attempts, user_name, history_count, loss_games)
"""
This is the main function of the game.
"""
def main():
    history_count, history_wins, fails, avg_score, loss_games = history_fails()
    history_words = load_history(HISTORY_FILE)
    attempts = 0
    # avg_score =

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
        history_count, history_wins, fails, avg_score, loss_games = history_fails()

     #   historic_attempts, history_count = history_attempts()
     #   avg_score = average_attempts(history_words)

        play_game(dev_debug, user_name, history_wins, avg_score, fails, history_count, loss_games) # DEBUG mode - remove for production

        # end_stat = len(history_words)
        # end_stat = end_stat + 1 # Increment total games played by 1 for the current game

        print_game_over()
        play_again = input(f"\nWow! How fun was that?\n\nShall we Play again, {user_name}? (y/n): \n")
    #    if play_again != 'y':
      #  print("\n\nAverage number of attempts on winning games: ", round(avg_score))
    #   #  print(f"\nThere have been out of ... there have been {fails} unsuccessful games\n")
    #   #  print(f"\nThere have been a total of {historic_attempts} successful games so far!\n")
    #     print(f"Total Games played: {end_stat}\nTotal Wins: {history_wins}\nTotal Loses: {fails}\n")
    #     print(f"Thanks for playing, {user_name}!\n\n")
        print_game_over()
        game_report(history_words, history_wins, avg_score, attempts, user_name, history_count, loss_games)
        print_game_name()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()

# # def average_attempts(historic_attempts, history_wins):
#     # Load history from file
#     history_words = load_history(HISTORY_FILE)

#     total_attempts = 0
#     win_count = 0

#     for entry in history_words:
#         # Format is like "3-USERNAME" for wins or "X-USERNAME" for fails
#         if entry.startswith('X-'):
#             continue  # Skip failed games

#         parts = entry.split('-')
#         if len(parts) >= 1:
#             try:
#                 attempts = int(parts[0])
#                 total_attempts += attempts
#     #             win_count += 1
#     #         except ValueError:
#     #             pass  # Ignore if can't convert
#             else:

#     # if win_count == 0:
#     #     return 0  # Avoid division by zero

#             return total_attempts / win_count

# # # Function to find
# # def_player_results():
# #     player_name = word.split("-")[0]  # Extract player name from the word
# #     player_score = word.split("-")[1]  # Extract player score from the word
# #     for valid_games in history_words:  # Calculate valid completed games
# #         for p in player_score in valid_games:
# #             if player_score in
# #                 return (min)player_score # find lowest player_score
# #             if player_name in min(player_score):
# #                 return player_name

# #     # Find player results in history
# #     for p in player_score in ["1", "2", "3", "4", "5"]:
# #     valid_games(player_score)
# #        min(player_score)
# #     # Winners list
# def def_player_results(history_words):
#     min_score = None
#     min_player = None
#     player_counts = {}
#     total_score = 0
#     total_wins = 0

#     for stat in history_words:
#         stat = word.split("-")
#         stat_player_name = word.split("-")[0]  # Extract player name from the word
#         stat_player_counts = {}  #

#         stat_player_score = word.split("-")[1]  # Extract player score from the word

#         # Count all players (for frequency)
#         stat_player_counts[stat_player_nameplayer_part}

#         # Ignore fails for score calculations
#         if score_part.upper() == 'X':
#             continue

#         if not score_part.is n player_score in ["1", "2", "3", "4", "5"]:
#             continue

#         score = int(score_part)

#         # Track lowest score and player
#         if min_score is None or score < min_score:
#             min_score = score
#             min_player = player_part

#         total_score += score
#         total_wins += 1

#     # Calculate average attempts, avoid division by zero
#     avg_attempts = total_score / total_wins if total_wins > 0 else 0

#     # Find most frequent player(s)
#     max_plays = max(player_counts.values()) if player_counts else 0
#     most_frequent_players = [p for p, count in player_counts.items() if count == max_plays]

#     return min_score, min_player, avg_attempts, most_frequent_players, len(history_words) - player_counts.get('X', 0)
