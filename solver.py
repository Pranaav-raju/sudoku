from collections import namedtuple
import copy

# A move has a row, column, and other options to play instead
Move = namedtuple('Move', 'row col options')

def _find_empty_spots(board):
    spots = []
    for row in xrange(9):
        spots.extend([(row, col) for col in xrange(9) if not board.board[row][col]])
    return spots

def _fill_simple(board):
    '''Fills all the spots on the board that only have one possible move.'''
    # Keep checking the full board as long as progress is being made
    while True:
        set_value = False
        for row, col in _find_empty_spots(board):
            remaining = board.valid_moves(row, col)
            if not remaining:
                # Dead-end position
                return None
            elif len(remaining) == 1:
                # Make move and continue
                board.board[row][col] = remaining.pop()
                set_value = True
        if not set_value:
            # The board is valid, but no more spaces can be filled this way
            return board

def solve(board):
    """
    Checks if board is valid, then solves if so.

    Returns:
        The solved board object if the board is valid and solvable.
        If the board is valid but not solvable, returns None.

    Raises:
        ValueError: The board has duplicate values in a row, column, or box.
    """
    # fill_board won't build an invalid board, so only check the initial board
    if not board._is_valid_board():
        raise ValueError("That board has duplicate values.")
    solutions = count_solutions(board)
    if not solutions:
        raise ValueError("That board has no valid solutions.")
    elif solutions > 1:
        raise ValueError("That board has more than one valid solution.")
    return fill_board(board)

def count_solutions(board):
    """
    Counts the number of solutions for this board, up to 2.

    If the count is 0, the board cannot be solved from the current configuration.

    This function aborts counting after 2 solutions are found.

    Returns:
        One of the integers 0, 1, or 2.
    """
    # Fill in all single-solution positions and check for unwinnable positions
    if not _fill_simple(board):
        return 0 # Unwinnable position
    for row, col in _find_empty_spots(board):
        # Keep track of solutions from each position; there should be
        #   multiple valid plays in different positions,
        #   since _fill_simple handled the zero and single move cases.
        solutions = 0
        for move in board.valid_moves(row, col):
            board_copy = copy.deepcopy(board)
            # Make the move on this board, but don't keep all the changes
            #    made by the recursive calls from here
            board_copy.board[row][col] = move
            if fill_board(board_copy):
                # If it's possible to fill the board after making this move,
                #   consider this move a valid solution
                solutions += 1
                if solutions >= 2:
                    return solutions
    # If solutions never reached more than 1, there is only one solution for the board
    return 1

# Recursive move searcher and implementer
def fill_board(board):
    """
    Fully solves the board, if possible, and returns the result.

    Returns:
        The solved board object if the board is solvable, None otherwise.
    """
    # Set a maximum value for moves remaining from a square
    smallest_move = float("inf")
    next_move = None
    if not _fill_simple(board):
        # Unwinnable board
        return None
    for row, col in _find_empty_spots(board):
        remaining = board.valid_moves(row, col)
        # Spots with fewer than 2 options are handled by _fill_simple,
        # so pick any of the most constrained remaining positions
        if len(remaining) < smallest_move:
            smallest_move = len(remaining)
            next_move = Move(row, col, remaining)
    # Check for won position; board must be valid because moves were
    #   chosen only from valid moves
    if not next_move:
        # Pass up the winning board
        return board
    for option in next_move.options:
        board_copy = copy.deepcopy(board)
        board_copy.board[next_move.row][next_move.col] = option
        # fill_board will attempt to fill the board passed to it.
        # If it's not successful, it will contain moves that don't lead to
        #   a valid solution, with no path to undoing them, so make a copy.
        end_result = fill_board(board_copy)
        # end_result will be None unless it is fully complete.
        if end_result:
            # Pass up the winning board
            return end_result
    return None