from flask import Flask, url_for, request
from flask import render_template
from board import Board
from solver import solve
import string

def build_puzzle_string(request_args):
    """Returns a tuple of (puzzle_string, error_message).

    Request_args is a dictionary of the URL request values.

    The first element in the tuple is the puzzle string.
    The second element is an error message if there was one,
        or an empty string otherwise.

    This function does not consider whether the resulting puzzle string
        is valid or has only a single solution.
    """
    board_letters = []
    digits = set(string.digits)
    error = ""
    for row in xrange(9):
        for col in xrange(9):
            cell = request_args.get(str(row) + str(col), '')
            if cell == "" or cell == "0":
                board_letters.append("0")
            elif cell not in digits: # '0' is in digits, so check that first
                error = cell + " is not a number in the range 0-9. "
                board_letters.append("0")
            else:
                board_letters.append(cell)
    return ("".join(board_letters), error)

app = Flask(__name__)
@app.route('/')
def index():
    if not request.args:
        print "Didn't find a request."
        return render_template('grid.html')
    digits = set(string.digits)
    BASE_ERROR = "<br>Please change the numbers and try again."
    error = '' # Error message to output on page, if there is one
    puzz_string = ""
    if 'puzzle' in request.args:
        puzz_string = request.args.get('puzzle')
        if len(puzz_string) > 81:
            error = "Puzzle strings must contain no more than 81 characters. " + BASE_ERROR
        elif (set(puzz_string) - digits) != set():
            error = "That string contains non-numeric characters. " + BASE_ERROR
        elif len(puzz_string) < 81:
            # Pad short string with trailing zeroes
            puzz_string += "0" * (81 - len(puzz_string))
        board_array = Board.string_to_array(puzz_string)
    else:
        # Handle cell-by-cell arguments
        # If request.args has non-puzzle items, but not 81 of them, it seems
        #   likely that someone appended invalid values to the URL.
        # build_puzzle_string ignores any extra arguments in the URL.
        puzz_string, error = build_puzzle_string(request.args)
        if error:
            error += BASE_ERROR
        # Create the rest of the board even if some of it was invalid
        board_array = Board.string_to_array(puzz_string)
    if not error:
        b = Board(board_array)
        try:
            solved = solve(b)
        except ValueError as e:
            error = str(e) + " " + BASE_ERROR
    if error: # Different from the above check because solve() might raise an error
        return render_template('grid.html', puzzle_string=puzz_string, error=error)
    return render_template('grid.html', puzzle_string=solved.to_puzzle_string(), solved=True)