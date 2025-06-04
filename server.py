from flask import Flask
import game

app = Flask(__name__)

@app.route("/")
def home():
    return game.main()  # return game output as string

if __name__ == "__main__":
    app.run()
