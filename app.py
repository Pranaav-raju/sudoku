from flask import Flask, url_for, request
from flask import render_template
import board
from solver import fill_board

app = Flask(__name__)

@app.route('/')
def index():
    if not request.args:
        print "Didn't find a request."
        return render_template('grid.html')
    boardstring = ""
    for row in xrange(9):
        for col in xrange(9):
            cell = request.args.get(str(row) + str(col), '')
            if cell == "":
                boardstring += "0"
            else:
                boardstring += cell
    board_array = board.Board.string_to_array(boardstring)
    b = board.Board(board_array)
    solved = str(fill_board(b))
    print 'Solved board is '
    print solved
    return render_template('grid.html', output=solved)