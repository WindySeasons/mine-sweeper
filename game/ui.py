import tkinter as tk
from game.board import Board
from game.settings import GRID_SIZE, CELL_SIZE, WINDOW_TITLE
import time
from threading import Thread

class MinesweeperUI:
    def __init__(self):
        self.board = Board()
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start_time = None
        self.timer_running = False
        self.timer_label = tk.Label(self.root, text="Time: 0s")
        self.timer_label.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE)
        self.restart_button = tk.Button(self.root, text="Restart", command=self._restart_game)
        self.restart_button.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE)
        self._create_widgets()

    def _create_widgets(self):
        """创建网格按钮"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                btn = tk.Button(self.root, width=2, height=1, command=lambda r=row, c=col: self._on_cell_click(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[row][col] = btn

    def _start_timer(self):
        """启动计时器"""
        self.start_time = time.time()
        self.timer_running = True
        Thread(target=self._update_timer, daemon=True).start()

    def _update_timer(self):
        """更新计时器显示"""
        while self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            time.sleep(1)

    def _stop_timer(self):
        """停止计时器"""
        self.timer_running = False

    def _on_cell_click(self, row, col):
        """处理单元格点击事件"""
        if self.start_time is None:
            self._start_timer()
        value = self.board.reveal_cell(row, col)
        if value == -1:
            self._stop_timer()
            self.buttons[row][col].config(text="💣", bg="red")
            self._game_over()
        else:
            self.buttons[row][col].config(text=str(value), state="disabled")

    def _game_over(self):
        """游戏结束"""
        self._stop_timer()
        for row, col in self.board.mines:
            self.buttons[row][col].config(text="💣", bg="red")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.buttons[row][col].config(state="disabled")

    def _restart_game(self):
        """重新开始游戏"""
        self._stop_timer()
        self.board = Board()  # 重置游戏逻辑
        self.start_time = None
        self.timer_label.config(text="Time: 0s")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.buttons[row][col].config(text="", bg="SystemButtonFace", state="normal")

    def run(self):
        """运行游戏"""
        self.root.mainloop()