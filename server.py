from flask import Flask, request, jsonify
import game  # your existing game.py

app = Flask(__name__)

# Example: keep game state per session (simplified)
game_state = None

@app.route('/play', methods=['POST'])
def play():
    global game_state
    data = request.json
    user_input = data.get('input', '')

    # Call your game function — you might need to adapt here
    # For example, if your game.py has a `game(input)` function:
    output = game.game(user_input)

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
