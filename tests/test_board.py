import unittest
from game.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        """在每个测试用例前初始化一个新的 Board 实例"""
        self.board = Board()

    def test_mine_distribution(self):
        """测试地雷分布是否正确"""
        self.assertEqual(len(self.board.mines), self.board.num_mines)

    def test_reveal_cell(self):
        """测试单元格揭示逻辑"""
        for row, col in self.board.mines:
            with self.subTest(row=row, col=col):
                self.assertEqual(self.board.reveal_cell(row, col), -1)  # 地雷单元格

    def test_victory_condition(self):
        """测试胜利条件"""
        for row in range(self.board.grid_size):
            for col in range(self.board.grid_size):
                if (row, col) not in self.board.mines:
                    self.board.reveal_cell(row, col)
        self.assertEqual(self.board.revealed_cells, self.board.grid_size**2 - self.board.num_mines)

if __name__ == "__main__":
    unittest.main()