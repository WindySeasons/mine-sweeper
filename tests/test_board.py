import unittest
from game.board import Board
from game.settings import GRID_SIZE, NUM_MINES

class TestBoard(unittest.TestCase):
    def test_victory_condition(self):
        """Test that the victory condition is met when all non-mine cells are revealed."""
        board = Board()

        # Simulate revealing all non-mine cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row, col) not in board.mines:
                    board.reveal_cell(row, col)

        # Check if the victory condition is met
        self.assertEqual(board.revealed_cells, GRID_SIZE * GRID_SIZE - NUM_MINES)

if __name__ == "__main__":
    unittest.main()