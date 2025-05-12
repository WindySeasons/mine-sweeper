import random
from game.settings import GRID_SIZE, NUM_MINES

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.mines = set()
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        """随机放置地雷"""
        while len(self.mines) < NUM_MINES:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                self.grid[row][col] = -1  # -1 表示地雷

    def _calculate_numbers(self):
        """计算每个单元格周围的地雷数量"""
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == -1:
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.grid[nr][nc] == -1:
                        count += 1
                self.grid[row][col] = count

    def reveal_cell(self, row, col):
        """揭示单元格，返回其值"""
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return self.grid[row][col]
        return None