from math import sqrt
import itertools

# This program only handles 9x9 standard-sized boards
BOARD_SIZE = 9
BOX_SIZE = 3

class Board(object):
    """Represents a Sudoku board."""

    def __init__(self, board_array):
        """Creates a new Sudoku puzzle board.

        Per the rules of Sudoku, each board consists of 9 squares, each
        of which contains 9 numbers in a 3x3 box. Each number appears
        exactly once in each 3x3 square, row, and column.
        Does not test whether board_array has duplicate values.

        Args:
            board_array: A 9x9 2D list containing the initial board setup.
            Blank spaces are represented by zeroes, and filled spaces are
            represented by integers 1-9.

        Raises:
            ValueError: board_array is not a valid board configuration.
        """
        # Raises an exception if not valid
        assert Board._is_valid_start_board(board_array)
        self.board = board_array

    def __str__(self):
        return "\n".join(" ".join(str(x) for x in row) for row in self.board)

    def to_dict(self):
        """Returns a dictionary of this Board's values.

        Format:
            board_dict["00"] returns the number at row 0, column 0.

        Unfilled positions have values of 0.
        """
        # Length 2 strings for all positions 00-88
        # Not using range(89) because of zero padding for first row
        allpos = itertools.product(xrange(9), repeat=2)
        board_dict = {str(x) + str(y):0 for x, y in allpos}
        for row in xrange(BOARD_SIZE):
            for col in xrange(BOARD_SIZE):
                cell_value = self.board[row][col]
                if cell_value:
                    board_dict[str(row) + str(col)] = cell_value
        return board_dict

    @staticmethod
    def string_to_array(board_string):
        """Converts a board string into 9x9 board array format.

        This function does not check the validity of the board array.

        Args:
            board_string: An 81-character string representing the rows of
                a board merged together, where the first character is the
                first character on the top row (the upper left number),
                the last character is the last character on the bottom row
                (the bottom right number), and zeroes represent empty spaces.

        Returns:
            A 2D array for use with the Board constructor.

        Raises:
            ValueError: board_string is not valid.
    """
        if len(board_string) != 81:
            raise ValueError("Board string must be 81 characters")
        rows = []
        for row_start in xrange(0, 73, 9):
            rows.append([int(num) for num in board_string[row_start:row_start + 9]])
        return rows

    @staticmethod
    def _is_valid_start_board(board_array):
        """Confirms that a board array is in valid Sudoku format.

        Does not confirm whether it is possible to solve this board.
        Does not confirm whether this board has duplicate values.

        Returns:
            True if board_array is in the valid format.

        Raises:
            TypeError: board_array is not a list or tuple.

            ValueError: board_array is not a valid board configuration.
        """
        if type(board_array) not in (list, tuple):
            raise TypeError("Board must be a 2D list or tuple")
        if len(board_array) != BOARD_SIZE:
            raise ValueError("Board must contain {} squares".format(BOARD_SIZE))
        valid_values = set(xrange(BOARD_SIZE + 1))
        for sublist in board_array:
            if type(sublist) not in (list, tuple):
                raise TypeError("Board must contain only lists or tuples")
            if len(sublist) != BOARD_SIZE:
                raise ValueError("Board boxes must be square")
            for item in sublist:
                if item not in valid_values:
                    raise ValueError(
                        "Board numbers must be integers in range " +
                        "0 <= x <= board size")
        return True

    def _is_valid_board(self):
        """Determines whether this Board is valid.

        A Board is considered valid if there are no repeating numbers
        (besides 0, which represents a blank space) in any row, column,
        or box of the board. Boxes must be square, and are 3 x 3 on
        a standard board.
        For a standard board, the 3 x 3 boxes divide the board into ninths
        such that exactly 9 fit onto the board. For example, there can be
        repeating numbers in the 3 columns that span indices 1-3, but not
        0-2, because 0-2 and 3-5 are separate boxes.

        Returns:
            True iff the board is valid, and False otherwise.
        """
        # We can't use _numbers_in_row, _numbers_in_column,or _numbers_in_box
        #   for these because those don't check for duplicates.
        # Check rows
        for i in xrange(BOARD_SIZE):
            row_numbers = set()
            for number in self.board[i]:
                if number in row_numbers:
                    return False
                if number: # Don't add 0
                    row_numbers.add(number)
        # Check columns
        for j in xrange(BOARD_SIZE):
            col_numbers = set()
            for i in xrange(BOARD_SIZE):
                number = self.board[i][j]
                if number in col_numbers:
                    return False
                if number: # Don't add 0
                    col_numbers.add(number)
        # Check boxes
        # Start at upper left of each box, then move one box width in each direction
        move_range = xrange(0, BOARD_SIZE, BOX_SIZE)
        boxes = [(x, y) for x in move_range for y in move_range]
        for box_x, box_y in boxes:
            box_numbers = set()
            for i in xrange(box_x, box_x + BOX_SIZE):
                for j in xrange(box_y, box_y + BOX_SIZE):
                    number = self.board[i][j]
                    if number in box_numbers:
                        return False
                    if number: # Don't add 0
                        box_numbers.add(number)
        return True

    def _numbers_in_row(self, row):
        """Returns a set of the numbers in this row.

        Zeroes are ignored, since they represent blank spaces.

        Args:
            row: The zero-indexed integer of the row of this board to check.
            Must be in the range 0 <= x < board_size, so 0 <= x < 9
            for a standard 9x9 board.

        Returns:
            A set of the non-zero numbers found in this row.

        Raises:
            IndexError: row is outside the valid range for this board.
        """
        if not self._valid_pos(row):
            raise IndexError("Row {} is not a valid integer".format(row))
        return set(self.board[row]) - set([0])

    def _numbers_in_column(self, col):
        """Returns a set of the numbers in this column.

        Zeroes are ignored, since they represent blank spaces.

        Args:
            col: The zero-indexed integer of the column of this board to check.
            Must be in the range 0 <= x < board_size, so 0 <= x < 9
            for a standard 9x9 board.

        Returns:
            A set of the non-zero numbers found in this column.

        Raises:
            IndexError: col is outside the valid range for this board.
        """
        if not self._valid_pos(col):
            raise IndexError("Column {} is not a valid integer".format(col))
        col_numbers = set()
        for i in xrange(BOARD_SIZE):
            if self.board[i][col]:
                col_numbers.add(self.board[i][col])
        return col_numbers

    def _numbers_in_box(self, box_start_row, box_start_col):
        """Returns a set of the numbers in the given box.

        Zeroes are ignored, since they represent blank spaces.

        For example, to check the first box, box_start_row and
        box_start_col should be 0 and 0. To check the center box,
        they should be 3 and 3.

        For a standard 9x9 board, the only acceptable values for box_start_row
        and box_start_col are 0, 3, and 6.

        Args:
            box_start_row: The row index of the upper left most number in the
              box.

            box_start_col: The column index of the upper left most number in
              the box.

        Returns:
            A set of the non-zero numbers found in this box.

        Raises:
            TypeError: box start values are not integers.

            IndexError: box start values are outside the valid range
               for this board.
        """
        # Don't use _valid_pos; box requirements are more specific
        size = BOARD_SIZE
        for start in (box_start_row, box_start_col):
            # Avoid hardcoding valid positions of (0, 3, 6)
            if (not (self._valid_pos(box_start_row) and self._valid_pos(box_start_col)) or
                not (0 <= start < size and start % BOX_SIZE == 0)):
                    raise IndexError("Invalid box start number: {}".format(start))
        box_numbers = set()
        for i in xrange(box_start_row, box_start_row + BOX_SIZE):
            for j in xrange(box_start_col, box_start_col + BOX_SIZE):
                if self.board[i][j]:
                    box_numbers.add(self.board[i][j])
        return box_numbers

    def valid_moves(self, row, column):
        """Returns the valid moves for the given position.

        Args:
            row, column: The zero-indexed integer row and column
            numbers for the position to check. Must be in the range
            0 <= x < board_size.

        Returns:
            A set of numbers in the range 1 to board size (inclusive)
            that are not already part of the given position's row,
            column, or box, and so can be played at the given position.

        Raises:
            IndexError: The position at row, column is not empty; it
            contains a number > 0.
        """
        if not (self._valid_pos(row) and self._valid_pos(column)):
            raise IndexError("Invalid row or column index.")
        if self.board[row][column]:
            raise IndexError(
                "Non-zero number already at position {},{}: {}".format(
                    row, column, self.board[row][column])
                )
        used_numbers = self._numbers_in_row(row)
        # Combine all the used numbers together because we don't care where
        # they were used, just that they are no longer possible
        used_numbers.update(self._numbers_in_column(column))
        # Round row and column numbers down to box start positions
        # TODO: Can I just do mod here?
        x = row / BOX_SIZE * BOX_SIZE
        y = column / BOX_SIZE * BOX_SIZE
        used_numbers.update(self._numbers_in_box(x, y))
        return set(xrange(1, BOARD_SIZE + 1)) - used_numbers

    def _valid_pos(self, index):
        """Checks whether the given index is valid for this Board.

        Args:
            index: integer, the index to check. A valid index is an integer in
            the range 0 <= x < board_size.

            Since all Boards must be square, a valid row number is a
            valid column number, and vice versa.

        Returns:
            True iff index is a valid row or column index.
        """
        return index in xrange(BOARD_SIZE)