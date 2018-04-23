from flask import Flask, url_for, request
from flask import render_template
from board import Board
from solver import solve
import string

def build_puzzle_string(request_args):
    """Returns a tuple of (success, string).

    Request_args is a dictionary of the URL request values.

    The first element in the tuple is True iff the string was built without errors.
    The second element is an error message if there was one,
        and the puzzle string otherwise.
    """
    board_letters = []
    digits = set(string.digits)
    for row in xrange(9):
        for col in xrange(9):
            cell = request_args.get(str(row) + str(col), '')
            if cell == "" or cell == "0":
                board_letters.append("0")
            elif cell not in digits:
                error = cell + " is not a number in the range 0-9. "
                return (False, error)
            else:
                board_letters.append(cell)
    return (True, "".join(board_letters))

app = Flask(__name__)
@app.route('/')
def index():
    # If request.args has non-puzzle items, but not 81 of them, it's likely that someone appended
    #   invalid values to the URL.
    # It's possible that someone just specified some of the cells and left the rest out
    #   of the argument list, but I don't see value in catering to that possibility.
    if not request.args:
        print "Didn't find a request."
        return render_template('grid.html')
    digits = set(string.digits)
    BASE_ERROR = "<br>Please try again or enter your board values manually."
    error = '' # Error message to output on page, if there is one
    if 'puzzle' in request.args:
        puzzle_string = request.args.get('puzzle')
        if len(puzzle_string) > 81:
            error = "Puzzle strings must contain no more than 81 characters. " + BASE_ERROR
        elif (set(puzzle_string) - digits) != set():
            error = "That string contains non-numeric characters. " + BASE_ERROR
        elif len(puzzle_string) < 81:
            # Pad short string with trailing zeroes
            puzzle_string += "0" * (81 - len(puzzle_string))
        board_array = Board.string_to_array(puzzle_string)
    else:
        # Any extra arguments are ignored
        success, result_string = build_puzzle_string(request.args)
        if success:
            board_array = Board.string_to_array(result_string)
        else:
            error = result_string + BASE_ERROR
    if not error:
        b = Board(board_array)
        try:
            solved = solve(b)
        except ValueError as e:
            error = str(e) + " " + BASE_ERROR
    if error: # Different from the above check because solve() might raise an error
        return render_template('grid.html', error=error)
    return render_template('result.html', output=solved.to_dict())