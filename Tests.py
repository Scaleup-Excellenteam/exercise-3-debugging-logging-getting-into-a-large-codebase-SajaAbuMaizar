from unittest.mock import Mock
from Piece import Knight
import pytest

from ai_engine import chess_ai
from enums import Player
from chess_engine import game_state


# Unit-tests:
def test_get_valid_peaceful_moves_empty_board():
    # Create a mock game state
    game_state = Mock()
    # Set the return value of get_piece to Player.EMPTY
    game_state.get_piece.return_value = Player.EMPTY

    # Create a knight object with player 1 at position (4, 4)
    knight = Knight(Player.PLAYER_1, 4, 4)

    # Get the valid peaceful moves for the knight
    moves = knight.get_valid_peaceful_moves(game_state)

    # Perform assertions
    assert len(moves) == 8  # Expecting 8 valid moves
    assert (2, 3) in moves  # Expecting (2, 3) to be a valid move
    assert (2, 5) in moves  # Expecting (2, 5) to be a valid move
    assert (3, 2) in moves  # Expecting (3, 2) to be a valid move
    assert (3, 6) in moves  # Expecting (3, 6) to be a valid move
    assert (5, 2) in moves  # Expecting (5, 2) to be a valid move
    assert (5, 6) in moves  # Expecting (5, 6) to be a valid move
    assert (6, 3) in moves  # Expecting (6, 3) to be a valid move
    assert (6, 5) in moves  # Expecting (6, 5) to be a valid move


def test_get_valid_peaceful_moves_corner():
    # Create a mock game state
    game_state = Mock()
    # Set the return value of get_piece to Player.EMPTY
    game_state.get_piece.return_value = Player.EMPTY

    # Create a knight object with player 1 at position (0, 0)
    knight = Knight(Player.PLAYER_1, 0, 0)

    # Get the valid peaceful moves for the knight
    moves = knight.get_valid_peaceful_moves(game_state)

    # Perform assertions
    assert len(moves) == 2  # Expecting 2 valid moves
    assert (1, 2) in moves  # Expecting (1, 2) to be a valid move


# integration-tests:

def test_get_valid_piece_moves():
    # Create a mock game state
    game_state = Mock()
    # Set the return value of get_piece to Player.EMPTY
    game_state.get_piece.return_value = Player.EMPTY

    # Create a knight object with player 1 at position (4, 4)
    knight = Knight(Player.PLAYER_1, 4, 4)

    # Set up the expected moves
    expected_peaceful_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    expected_piece_takes = []
    expected_moves = expected_peaceful_moves + expected_piece_takes

    # Get the valid piece moves for the knight
    moves = knight.get_valid_piece_moves(game_state)

    # Perform assertions
    assert moves == expected_moves


def test_evaluate_board(player):
    # Create a mock game state
    game_state = Mock()

    # Create a chess_ai object
    ai = chess_ai()

    # Set up the expected evaluation score
    expected_score = 0

    # Iterate over the board positions
    for row in range(8):
        for col in range(8):
            # Mock the piece object
            piece = Mock()

            # Mock the is_valid_piece method
            game_state.is_valid_piece.return_value = True

            # Set the return value of get_piece to the mocked piece
            game_state.get_piece.return_value = piece

            # Set the return value of is_player based on the player argument
            piece.is_player.return_value = True if player == Player.PLAYER_1 else False

            # Set the return value of get_name based on the piece name
            piece.get_name.return_value = "k"  # Replace with the appropriate piece name

            # Determine the expected piece value based on the player and piece name
            piece_value = -1000  # Replace with the appropriate piece value

            # Add the expected piece value to the evaluation score
            expected_score += piece_value

    # Call the evaluate_board function
    score = ai.evaluate_board(game_state, player)

    # Perform assertion
    assert score == expected_score


# System test

def system_test():
    # Create a new game
    game = game_state()

    # Make a sequence of moves
    moves = [
        ((6, 4), (4, 4)),  # Player 1 pawn moves forward
        ((1, 3), (3, 3)),  # Player 2 pawn moves forward
        ((6, 3), (4, 3)),  # Player 1 pawn moves forward
        ((0, 5), (4, 1)),  # Player 2 queen captures player 1 pawn
        ((7, 4), (5, 4)),  # Player 1 king moves forward
        ((4, 1), (3, 2)),  # Player 2 queen captures player 1 pawn
        ((5, 4), (4, 4)),  # Player 1 king moves back
        ((3, 2), (2, 3)),  # Player 2 queen captures player 1 pawn
        ((4, 4), (3, 4)),  # Player 1 king moves back
        ((2, 3), (3, 3)),  # Player 2 queen captures player 1 pawn
        ((3, 4), (4, 4)),  # Player 1 king moves forward
        ((3, 3), (4, 3)),  # Player 2 queen captures player 1 pawn
        ((4, 4), (5, 4)),  # Player 1 king moves forward
        ((4, 3), (5, 3)),  # Player 2 queen captures player 1 pawn
        ((5, 4), (6, 4)),  # Player 1 king moves forward
        ((5, 3), (6, 3)),  # Player 2 queen captures player 1 pawn
        ((6, 4), (7, 4)),  # Player 1 king moves forward
        ((6, 3), (7, 3)),  # Player 2 queen captures player 1 pawn
        ((7, 4), (7, 3)),  # Player 1 king captures player 2 queen
        ((7, 3), (7, 4)),  # Player 1 king moves back
        ((7, 4), (6, 4))  # Player 1 king moves back
    ]

    # Execute the moves
    for move in moves:
        starting_square, ending_square = move
        game.move_piece(starting_square, ending_square, False)
