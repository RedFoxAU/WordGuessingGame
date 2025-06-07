# def print_user_counts():
#     history_user_counts = {}
#     lines = load_history(HISTORY_FILE)

#     for line in lines:
#         line = line.strip()
#         if len(line) > 2:
#             history_user = line[2:]  # Ignore first two characters to get name
#             if history_user in history_user_counts:
#                 history_user_counts[history_user] += 1
#             else:
#                 history_user_counts[history_user] = 1

#     print("\n--- User Game Counts:")
#     for history_user_counts in history_user_counts:
#         print(f"{history_user}: {history_user_counts[history_user]} games")

# def count_games():
#     with open(HISTORY_FILE, 'r') as f:
#         history_lines = [entry.strip() for entry in f.read().split()]
#     c_games_played = len(history_lines)
#     c_games_failed = 0
#     for x_entry in history_lines:
#         if x_entry.startswith('X-'):
#             c_games_failed += 1
#     c_games_won = c_games_played - c_games_failed

#     return c_games_played, c_games_won

# def user_mvp_game_count():
#     with open(HISTORY_FILE, 'r') as f:
#         history_lines = [entry.strip() for entry in f.read().split()]

#     games_failed = 0
#     for line in history_lines:
#         if line.startswith("X-"):
#             games_failed = games_failed + 1

#     games_total = len(history_lines)
#     games_won = games_total - games_failed

#     return games_total, games_won, games_failed

# def rank_summary():
#     with open(HISTORY_FILE, 'r') as f:
#         history_lines = [entry.strip() for entry in f.read().split()]

#     rank_counts = {
#         "1": 0,
#         "2": 0,
#         "3": 0,
#         "4": 0,
#         "5": 0
#     }

#     for line in history_lines:
#         if line.startswith("X-"):
#             pass
#         else:
#             first_char = line[0]
#             if first_char in rank_counts:
#                 rank_counts[first_char] += 1

#     print("\nWinners Tally:")
#     print("1 = Unbelievable! First Guess!! :", rank_counts["1"])
#     print("2 = Two guesses? Amazing        :", rank_counts["2"])
#     print("3 = You are a thinker!          :", rank_counts["3"])
#     print("4 = Great work!                 :", rank_counts["4"])
#     print("5 = You made it with 0 left!    :", rank_counts["5"])

# def first_lowest_score():
#     with open(HISTORY_FILE, 'r') as f:
#         history_lines = [line.strip() for line in f.read().split()]

#     lowest_score = None
#     mvp_user = None

#     for line in history_lines:
#         if line.startswith("X-"):
#             continue

#         score_name = line.split("-")
#         if len(score_name) == 2:
#             score = score_name[0]
#             name = score_name[1]

#             if lowest_score is None or score < lowest_score:
#                 lowest_score = score
#                 mvp_user = name

#     return lowest_score, mvp_user



, games_played, mvp_user, lowest_score)

        # Refresh stats after each game
        games_played, games_won = count_games()
        lowest_score, mvp_user = first_lowest_score()

        print(f"\nBest score was: {lowest_score}")
        print(f"First to get it: {mvp_user}")



    games_played, games_won = count_games()               # << load stats from file
    lowest_score, mvp_user = first_lowest_score()         # << load mvp info from file
