import random
from game.settings import GRID_ROWS, GRID_COLS, NUM_MINES

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.mines = set()
        self.revealed_cells = 0  # Track the number of revealed cells
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        """随机放置地雷"""
        while len(self.mines) < NUM_MINES:
            row = random.randint(0, GRID_ROWS - 1)
            col = random.randint(0, GRID_COLS - 1)
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
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if self.grid[row][col] == -1:
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and self.grid[nr][nc] == -1:
                        count += 1
                self.grid[row][col] = count

    def reveal_cell(self, row, col):
        """揭示单元格，返回其值"""
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
            if self.grid[row][col] != -1:  # Only count non-mine cells
                self.revealed_cells += 1
            return self.grid[row][col]
        return None#这里有问题要修改

    def update_board(self, rows, cols, num_mines):
        """更新棋盘大小和地雷数量"""
        global GRID_ROWS, GRID_COLS, NUM_MINES
        GRID_ROWS = rows
        GRID_COLS = cols
        NUM_MINES = num_mines

        # 重置棋盘
        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.mines = set()
        self.revealed_cells = 0

        # 重新放置地雷并计算数字
        self._place_mines()
        self._calculate_numbers()

# TODO: 优化地雷分布算法，确保更均匀的分布