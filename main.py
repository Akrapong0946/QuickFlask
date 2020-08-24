from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board, BasePiece, MoveError, MoveHistory, Move

def split_and_convert(inputstr):
    '''Convert 5-char inputstr into start and end tuples.'''
    start, end = inputstr.split(' ')
    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))
    return (start, end)

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
    start, end = split_and_convert(player_move)
    # TODO: Validate move, display error msg if move is invalid
    try:
        game.update(start, end)
        switch = True
    # Removing the error statement after a valid input
        ui.errmsg = None
    except MoveError:
        ui.errmsg = 'Invalid move, try again.'
        switch = False
    # TODO: Update the game object and ui object
    if switch:
        ui.board = game.display()
        game.next_turn()
    ui.inputlabel = f'{game.turn} player: '

    return render_template('chess.html', ui=ui)

@app.route('/promote', methods=['POST'])
def promote():
    # get player's promoted piece from POST request object
    # promotedpiece = request.form['promotion']
    # promotedpiece = promotedpiece.lower()[1]

app.run('0.0.0.0')