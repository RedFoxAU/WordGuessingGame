import js

async def input(prompt=""):
    print(prompt, end="")
    return await js.waitInput()

async def main():
    print("Welcome to Mini Word Guess Game!")
    word = "apple"
    guess = ""
    attempts = 0

    while guess != word:
        guess = (await input("Enter your 5-letter guess: ")).strip().lower()
        attempts += 1
        if guess == word:
            print(f"Correct! You got it in {attempts} tries.")
        else:
            print("Incorrect, try again.")
