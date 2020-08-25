from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board, BasePiece, MoveError, MoveHistory, Move

def split_and_convert(inputstr):
    '''Convert 5-char inputstr into start and end tuples.'''
    if (len(inputstr) == 5) and (inputstr[2] == ' '):
        start, end = inputstr.split(' ')
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        return (start, end)
    else:
        return MoveError


app = Flask(__name__)
ui = WebInterface()
game = Board()
movehistory = MoveHistory(100)

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

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        player_move = request.form['player_input']

        # TODO: Validate move, display error msg if move is invalid
        try:
            start, end = split_and_convert(player_move)
            encapped_move = Move(start, end)
            game.update(encapped_move.start, encapped_move.end)
        # Removing the error statement after a valid input
            ui.errmsg = None
        except:
            ui.errmsg = 'Invalid move, try again.'
            return render_template('chess.html', ui=ui)
        else:
            game.next_turn()
            movehistory.push(encapped_move)
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    return render_template('chess.html', ui=ui)

@app.route('/promote', methods=['POST'])
def promote():
    # get player's promoted piece from POST request object
    # promotedpiece = request.form['promotion']
    # promotedpiece = promotedpiece.lower()[1]
    pass

@app.route('/undo')
def undo():
    # Extract previous move
    popped_move = movehistory.pop()
    # Revert the piece movement
    game.move(popped_move.end, popped_move.start)
    # Revert turn to previous player (same as the next player)
    game.next_turn()
    return redirect('/play')

app.run('0.0.0.0')