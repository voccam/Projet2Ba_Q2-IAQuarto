import pytest
from joueur import is_winning_move, evaluate_board, piece_dangereuse

# === Fixtures ===
@pytest.fixture
def empty_board():
    return [None] * 16

@pytest.fixture
def full_board():
    return [
        "BDER", "SLEC", "BFPC", "SLPC",
        "BLFC", "SLER", "SDER", "SDFP",
        "BDER", "SLFC", "SDFR", "BDPC",
        "SLER", "BDER", "SLPC", "BDPC"
    ]

# === Tests unitaires ===

def test_is_winning_move_empty(empty_board):
    assert not is_winning_move(empty_board, 0, "BDER")

def test_is_winning_move_win_row():
    board = [None]*16
    board[0:3] = ["BDER", "BDER", "BDER"]
    assert is_winning_move(board, 3, "BDER")

def test_is_winning_move_diagonal():
    board = [None]*16
    board[0] = board[5] = board[10] = "BDER"
    assert is_winning_move(board, 15, "BDER")

def test_evaluate_board_empty(empty_board):
    assert evaluate_board(empty_board) == 0

def test_evaluate_board_with_two_common():
    board = [None]*16
    board[0] = "BDER"
    board[1] = "BDER"
    assert evaluate_board(board) > 0

def test_piece_dangereuse_detects_threat():
    board = [None]*16
    board[0:3] = ["BDER", "BDER", "BDER"]
    assert piece_dangereuse(board, "BDER")

def test_piece_dangereuse_safe():
    board = [None]*16
    board[0:3] = ["BDER", "SLPC", "SLEC"]
    assert not piece_dangereuse(board, "SLER")

import pytest
from joueur import is_winning_move, evaluate_board, piece_dangereuse, toutes_les_pieces, choisir_coup

def test_toutes_les_pieces_count():
    pieces = toutes_les_pieces()
    assert isinstance(pieces, set)
    assert len(pieces) == 16
    assert all(len(p) == 4 for p in pieces)

def test_choisir_coup_response_structure():
    board = [None] * 16
    state = {"board": board, "piece": "BDPC"}
    coup = choisir_coup(state)
    assert coup["response"] == "move"
    assert isinstance(coup["move"]["pos"], int)
    assert isinstance(coup["move"]["piece"], str)
    assert len(coup["move"]["piece"]) == 4