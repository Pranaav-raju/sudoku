from flask import Flask, url_for, request
from flask import render_template
from board import Board
from solver import solve

app = Flask(__name__)

@app.route('/')
def index():
    if not request.args:
        print "Didn't find a request."
        return render_template('grid.html')
    board_letters = []
    for row in xrange(9):
        for col in xrange(9):
            cell = request.args.get(str(row) + str(col), '')
            if cell == "" or cell == "0":
                board_letters.append("0")
            else:
                board_letters.append(cell)
    board_array = Board.string_to_array("".join(board_letters))
    b = Board(board_array)
    try:
        solved = solve(b)
    except ValueError:
        return render_template('grid.html', error="That board has duplicate values; please try entering them manually.")
    return render_template('result.html', output=solved.to_dict())