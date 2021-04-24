from flask import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    # since we're using flask, flask will turn the below into JSON automatically
    return {"gameId": game_id, "board": game.board}


@app.route('/api/score-word', methods=['POST'])
def validate_word():
    """
    handles API POST request
    requires the following data:
        { 
        gameID: gameId,
        word: word
        }

    Returns JSON: {result: "not-word | not-on-board | ok"}
    
    """

    word_to_check = request.json["word"]
    game_id = request.json["gameId"]
    current_game = games[game_id]
    # breakpoint()
    # create some variables to store if the word is in the word list
    # and if the word is on the current game board
    valid_word = current_game.is_word_in_word_list(word_to_check)
    word_on_board = current_game.check_word_on_board(word_to_check)

    if not valid_word:
        return jsonify({"result": "not-word"})
    elif not word_on_board:
        return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "ok"})