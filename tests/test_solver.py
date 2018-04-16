import random
from nose.tools import assert_equals
from parameterized import parameterized
from board import Board
from solver import fill_board
from solver import _find_empty_spots
import copy

# These boards don't need to be accessible to more than one test,
#   but it would be less readable to have these large arrays in
#   the parameterize decorator.
# Boards taken from online sudoku generators:
# Easy
board1 = Board([
                   [0, 0, 0, 0, 9, 0, 0, 5, 2],
                   [0, 1, 0, 0, 0, 0, 3, 0, 4],
                   [0, 0, 2, 3, 1, 5, 0, 0, 9],
                   [0, 0, 8, 7, 4, 6, 0, 3, 0],
                   [0, 7, 0, 9, 0, 1, 0, 2, 0],
                   [0, 9, 0, 2, 5, 3, 7, 0, 0],
                   [4, 0, 0, 5, 3, 8, 2, 0, 0],
                   [2, 0, 3, 0, 0, 0, 0, 6, 0],
                   [1, 5, 0, 0, 6, 0, 0, 0, 0]
                  ])
board1_result = Board([
                      [7, 3, 6, 8, 9, 4, 1, 5, 2],
                      [9, 1, 5, 6, 2, 7, 3, 8, 4],
                      [8, 4, 2, 3, 1, 5, 6, 7, 9],
                      [5, 2, 8, 7, 4, 6, 9, 3, 1],
                      [3, 7, 4, 9, 8, 1, 5, 2, 6],
                      [6, 9, 1, 2, 5, 3, 7, 4, 8],
                      [4, 6, 9, 5, 3, 8, 2, 1, 7],
                      [2, 8, 3, 1, 7, 9, 4, 6, 5],
                      [1, 5, 7, 4, 6, 2, 8, 9, 3]
                      ])
# Medium
board2 = Board([
                   [4, 0, 6, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 9, 0, 0, 8, 0, 1],
                   [8, 0, 0, 0, 7, 5, 0, 2, 0],
                   [0, 0, 5, 0, 6, 0, 0, 0, 8],
                   [2, 6, 0, 0, 9, 0, 0, 3, 4],
                   [9, 0, 0, 0, 2, 0, 7, 0, 0],
                   [0, 1, 0, 2, 5, 0, 0, 0, 7],
                   [6, 0, 9, 0, 0, 3, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 0, 3]
                ])
board2_result = Board([
                    [4, 9, 6, 1, 8, 2, 3, 7, 5],
                    [5, 7, 2, 9, 3, 6, 8, 4, 1],
                    [8, 3, 1, 4, 7, 5, 6, 2, 9],
                    [1, 4, 5, 3, 6, 7, 2, 9, 8],
                    [2, 6, 7, 8, 9, 1, 5, 3, 4],
                    [9, 8, 3, 5, 2, 4, 7, 1, 6],
                    [3, 1, 4, 2, 5, 8, 9, 6, 7],
                    [6, 5, 9, 7, 1, 3, 4, 8, 2],
                    [7, 2, 8, 6, 4, 9, 1, 5, 3]
                    ])
# Hard
board3 = Board([
                   [8, 9, 0, 0, 3, 4, 0, 0, 0],
                   [0, 0, 0, 0, 0, 8, 2, 0, 0],
                   [4, 0, 0, 2, 0, 0, 0, 0, 9],
                   [0, 3, 0, 0, 0, 0, 0, 2, 5],
                   [0, 0, 7, 0, 6, 0, 4, 0, 0],
                   [5, 1, 0, 0, 0, 0, 0, 6, 0],
                   [1, 0, 0, 0, 0, 3, 0, 0, 4],
                   [0, 0, 9, 7, 0, 0, 0, 0, 0],
                   [0, 0, 0, 6, 1, 0, 0, 7, 2],
              ])
board3_result = Board([
                      [8, 9, 2, 1, 3, 4, 7, 5, 6],
                      [7, 6, 3, 9, 5, 8, 2, 4, 1],
                      [4, 5, 1, 2, 7, 6, 3, 8, 9],
                      [6, 3, 8, 4, 9, 7, 1, 2, 5],
                      [9, 2, 7, 5, 6, 1, 4, 3, 8],
                      [5, 1, 4, 3, 8, 2, 9, 6, 7],
                      [1, 7, 6, 8, 2, 3, 5, 9, 4],
                      [2, 8, 9, 7, 4, 5, 6, 1, 3],
                      [3, 4, 5, 6, 1, 9, 8, 7, 2]
                      ])
# Expert
board4 = Board([
                   [0, 6, 0, 0, 2, 0, 0, 0, 0],
                   [0, 0, 2, 0, 0, 0, 0, 0, 5],
                   [0, 0, 0, 0, 3, 5, 8, 0, 0],
                   [5, 0, 0, 0, 7, 4, 0, 0, 6],
                   [0, 0, 0, 0, 0, 0, 0, 9, 8],
                   [0, 3, 9, 5, 0, 0, 0, 1, 0],
                   [0, 5, 0, 0, 6, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 7, 0, 4, 0],
                   [0, 4, 8, 0, 0, 0, 2, 0, 0]
                ])
board4_result = Board([
                       [8, 6, 5, 7, 2, 9, 4, 3, 1],
                       [3, 1, 2, 6, 4, 8, 9, 7, 5],
                       [7, 9, 4, 1, 3, 5, 8, 6, 2],
                       [5, 8, 1, 9, 7, 4, 3, 2, 6],
                       [4, 7, 6, 2, 1, 3, 5, 9, 8],
                       [2, 3, 9, 5, 8, 6, 7, 1, 4],
                       [9, 5, 7, 4, 6, 2, 1, 8, 3],
                       [1, 2, 3, 8, 5, 7, 6, 4, 9],
                       [6, 4, 8, 3, 9, 1, 2, 5, 7]
                      ])
# "World's Hardest Sudoku"
# https://www.kristanix.com/sudokuepic/worlds-hardest-sudoku.php
board5 = Board([
                [1, 0, 0, 0, 0, 7, 0, 9, 0],
                [0, 3, 0, 0, 2, 0, 0, 0, 8],
                [0, 0, 9, 6, 0, 0, 5, 0, 0],
                [0, 0, 5, 3, 0, 0, 9, 0, 0],
                [0, 1, 0, 0, 8, 0, 0, 0, 2],
                [6, 0, 0, 0, 0, 4, 0, 0, 0],
                [3, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 7],
                [0, 0, 7, 0, 0, 0, 3, 0, 0]
             ])
board5_result = Board([
                      [1, 6, 2, 8, 5, 7, 4, 9, 3],
                      [5, 3, 4, 1, 2, 9, 6, 7, 8],
                      [7, 8, 9, 6, 4, 3, 5, 2, 1],
                      [4, 7, 5, 3, 1, 2, 9, 8, 6],
                      [9, 1, 3, 5, 8, 6, 7, 4, 2],
                      [6, 2, 8, 7, 9, 4, 1, 3, 5],
                      [3, 5, 6, 4, 7, 8, 2, 1, 9],
                      [2, 4, 1, 9, 3, 5, 8, 6, 7],
                      [8, 9, 7, 2, 6, 1, 3, 5, 4]
])
@parameterized([
    (board1, board1_result),
    (board2, board2_result),
    (board3, board3_result),
    (board4, board4_result),
    (board5, board5_result),
])
def test_fill_board_samples(start_board, result_board):
    # The solved board is not the same Board object as the already-solved
    #   Board, so compare their underlying arrays
    board_copy = copy.deepcopy(start_board)
    assert_equals(fill_board(board_copy).board, result_board.board)

def test_fill_board_failed_board():
    input_array = [
                   # Second number on first row has no moves left
                   [3, 0, 7, 6, 9, 4, 1, 5, 2],
                   [5, 1, 9, 0, 7, 0, 3, 8, 4],
                   [8, 6, 2, 3, 1, 5, 0, 0, 9],
                   [0, 0, 8, 7, 4, 6, 0, 3, 0],
                   [0, 7, 0, 9, 0, 1, 0, 2, 0],
                   [0, 9, 0, 2, 5, 3, 7, 0, 0],
                   [4, 0, 0, 5, 3, 8, 2, 0, 0],
                   [2, 0, 3, 0, 0, 0, 0, 6, 0],
                   [1, 5, 0, 0, 6, 0, 0, 0, 0]
                  ]
    b = Board(input_array)
    assert not fill_board(b)

# TODO: Test solving randomly generated boards

def test_find_empty_spots_filled():
    for b in (board1_result, board2_result, board3_result, board4_result,
              board5_result):
        assert_equals(_find_empty_spots(b), [])

# Only one spot
# Spot in first row, spot in last row
# Spot in first col, spot in last col
# All spots
def test_find_empty_spots_single():
    b = Board([
                      [8, 9, 2, 1, 3, 4, 7, 5, 6],
                      [7, 6, 3, 0, 5, 8, 2, 4, 1],
                      [4, 5, 1, 2, 7, 6, 3, 8, 9],
                      [6, 3, 8, 4, 9, 7, 1, 2, 5],
                      [9, 2, 7, 5, 6, 1, 4, 3, 8],
                      [5, 1, 4, 3, 8, 2, 9, 6, 7],
                      [1, 7, 6, 8, 2, 3, 5, 9, 4],
                      [2, 8, 9, 7, 4, 5, 6, 1, 3],
                      [3, 4, 5, 6, 1, 9, 8, 7, 2]
                      ])
    assert_equals(_find_empty_spots(b), [(1, 3)])

def test_find_empty_spots_edge_rows():
    b = Board([
                      [8, 9, 0, 1, 3, 4, 7, 5, 6],
                      [7, 6, 3, 9, 5, 8, 2, 4, 1],
                      [4, 5, 1, 2, 7, 6, 3, 8, 9],
                      [6, 3, 8, 4, 9, 7, 1, 2, 5],
                      [9, 2, 7, 5, 6, 1, 4, 3, 8],
                      [5, 1, 4, 3, 8, 2, 9, 6, 7],
                      [1, 7, 6, 8, 2, 3, 5, 9, 4],
                      [2, 8, 9, 7, 4, 5, 6, 1, 3],
                      [3, 4, 5, 6, 1, 9, 0, 7, 2]
                      ])
    assert_equals(_find_empty_spots(b), [(0, 2), (8, 6)])