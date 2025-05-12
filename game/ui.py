import tkinter as tk
from tkinter import messagebox
from game.board import Board
from game.settings import GRID_SIZE, CELL_SIZE, WINDOW_TITLE, NUM_MINES
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
        self.game_over = False
        self.remaining_flags = NUM_MINES
        self.flags_label = tk.Label(self.root, text=f"Flags: {self.remaining_flags}")
        self.flags_label.grid(row=GRID_SIZE + 2, column=0, columnspan=GRID_SIZE)
        self._create_widgets()
        self._create_menu()

    def _create_widgets(self):
        """创建网格按钮"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                btn = tk.Button(self.root, width=2, height=1)
                btn.grid(row=row, column=col, padx=1, pady=1)
                btn.bind("<Button-1>", lambda event, r=row, c=col: self._on_left_click(r, c))
                btn.bind("<Button-3>", lambda event, r=row, c=col: self._on_right_click(r, c))
                self.buttons[row][col] = btn

    def _create_menu(self):
        """创建菜单栏"""
        menu_bar = tk.Menu(self.root)

        # 游戏菜单
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="重新开始", command=self._restart_game)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.root.quit)
        menu_bar.add_cascade(label="游戏", menu=game_menu)

        # 帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="关于", command=self._show_about)
        menu_bar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menu_bar)

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

    def _reveal_zeros(self, row, col, visited):
        """递归揭示值为 0 的单元格及其周围的单元格"""
        if (row, col) in visited:
            return
        visited.add((row, col))

        value = self.board.reveal_cell(row, col)
        self.buttons[row][col].config(text=str(value), state="disabled", bg="lightgrey")

        if value == 0:
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),         (0, 1),
                (1, -1), (1, 0), (1, 1)
            ]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    self._reveal_zeros(nr, nc, visited)

    def _on_left_click(self, row, col):
        """处理左键点击事件"""
        if self.game_over:
            return

        if self.start_time is None:
            self._start_timer()

        value = self.board.reveal_cell(row, col)
        if value == -1:
            self._stop_timer()
            self.buttons[row][col].config(text="💣", bg="red")
            self._game_over()
        elif value == 0:
            self._reveal_zeros(row, col, set())
        else:
            self.buttons[row][col].config(text=str(value), state="disabled")

    def _update_flags_label(self):
        """更新标记数量显示"""
        self.flags_label.config(text=f"Flags: {self.remaining_flags}")

    def _on_right_click(self, row, col):
        """处理右键点击事件"""
        if self.game_over:
            return

        btn = self.buttons[row][col]
        if btn["state"] == "disabled":
            return

        if btn["text"] == "🚩":
            btn.config(text="", bg="SystemButtonFace")
            self.remaining_flags += 1
        else:
            if self.remaining_flags > 0:
                btn.config(text="🚩", bg="yellow")
                self.remaining_flags -= 1
            else:
                return

        self._update_flags_label()

    def _game_over(self):
        """游戏结束"""
        self._stop_timer()
        self.game_over = True
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
        self.game_over = False
        self.remaining_flags = NUM_MINES
        self.timer_label.config(text="Time: 0s")
        self.flags_label.config(text=f"Flags: {self.remaining_flags}")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.buttons[row][col].config(text="", bg="SystemButtonFace", state="normal")

    def _show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", "扫雷游戏\n作者: 你的名字\n版本: 1.0")

    def run(self):
        """运行游戏"""
        self.root.mainloop()