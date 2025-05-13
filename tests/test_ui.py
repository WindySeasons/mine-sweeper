import unittest
from game.ui import UI

class TestUI(unittest.TestCase):
    def test_game_won(self):
        """Test that the game triggers a victory when all non-mine cells are revealed."""
        ui = UI()
        ui.revealed_cells = ui.GRID_SIZE * ui.GRID_SIZE - ui.NUM_MINES

        # Simulate the game won condition
        ui._game_won()

        # Check if the victory message or state is triggered
        self.assertTrue(ui.is_game_won)

if __name__ == "__main__":
    unittest.main()