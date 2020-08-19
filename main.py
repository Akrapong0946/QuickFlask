from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board

app = Flask(__name__)
ui = WebInterface()
game = Board()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    game.start()
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    ui.btnlabel = 'Move'
    return render_template('chess.html', ui=ui)

@app.route('/play', methods=['POST'])
def play():
    # TODO: get player move from POST request object
    player_move = request.form['player_input']
    # TODO: convert player input to start & end coord
    # TODO: Validate move, display error msg if move is invalid
    # TODO: Update the game object and ui object
    return render_template('chess.html', ui=ui)
   

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')