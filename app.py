from flask import Flask, url_for, request
from flask import render_template
import board
from solver import fill_board

app = Flask(__name__)

@app.route('/')
def index():
    if not request.args:
        print "Didn't find a request."
    row1 = request.args.get('row1', '')
    row1 += "0" * 72
    try:
        board_array = board.Board.string_to_array(row1)
    except ValueError:
        error = "Board {} is not 81 characters.".format(row1)
        print error
        return render_template('index.html', error=error)
    b = board.Board(board_array)
    solved = str(fill_board(b))
    print 'Solved board is '
    print solved
    return render_template('index.html', output=solved)