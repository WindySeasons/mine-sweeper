import tkinter as tk
from tkinter import messagebox
from game.board import Board
from game.settings import GRID_ROWS, GRID_COLS, CELL_SIZE, WINDOW_TITLE, NUM_MINES
import time
from threading import Thread
from game.records import load_records, save_records
import logging
import sys
import os

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MinesweeperUI:
    def __init__(self):
        self.board = Board()
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)

        # 动态设置图标路径
        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, "assets/images/icon.ico")
        else:
            icon_path = "assets/images/icon.ico"

        self.root.iconbitmap(icon_path)  # 设置任务栏图标

        # 创建菜单下方、网格上方的容器
        top_frame = tk.Frame(self.root)
        top_frame.grid(row=0, column=0, columnspan=GRID_COLS, pady=5)
        self.remaining_flags=NUM_MINES
        self.flags_label = tk.Label(top_frame, text=f"Flags: {self.remaining_flags}")
        self.flags_label.grid(row=0, column=0, padx=10)


        self.restart_button = tk.Button(top_frame, text="Restart", command=self._restart_game)
        self.restart_button.grid(row=0, column=1, padx=10)
        self.game_over=False

        self.start_time=None
        self.timer_running=False
        self.timer_label = tk.Label(top_frame, text="Time: 0s")
        self.timer_label.grid(row=0, column=2, padx=10)


        self.difficulty="初级"  #默认难度
        # 调整网格按钮的布局位置
        self.buttons = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self._create_widgets()
        self._create_menu()

        self.revealed_cells = 0  # 记录已揭示的非雷单元格数量
        self.best_times = load_records()  # 加载记录数据
        self.visited = set()  # 初始化已揭示格子的集合

    def _create_widgets(self):
        """创建网格按钮"""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                btn = tk.Button(self.root, width=2, height=1)
                btn.grid(row=row + 1, column=col, padx=1, pady=1)  # 调整行号以适应顶部容器
                btn.bind("<Button-1>", lambda event, r=row, c=col: self._on_left_click(r, c))
                btn.bind("<Button-3>", lambda event, r=row, c=col: self._on_right_click(r, c))
                self.buttons[row][col] = btn

    def _create_menu(self):
        """创建菜单栏"""
        menu_bar = tk.Menu(self.root)

        # 游戏菜单
        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="重新开始", command=self._restart_game)

        # 难度设置子菜单
        difficulty_menu = tk.Menu(game_menu, tearoff=0)
        difficulty_menu.add_command(label="初级 (9x9, 10 雷)", command=lambda: self._set_difficulty("初级"))
        difficulty_menu.add_command(label="中级 (16x16, 40 雷)", command=lambda: self._set_difficulty("中级"))
        difficulty_menu.add_command(label="高级 (16x30, 99 雷)", command=lambda: self._set_difficulty("高级"))
        difficulty_menu.add_command(label="自定义", command=self._custom_difficulty)
        game_menu.add_cascade(label="难度", menu=difficulty_menu)

        game_menu.add_separator()
        game_menu.add_command(label="扫雷英雄榜", command=self._show_records)
        # 根据 IS_TEST_VERSION 决定是否显示测试选项
        import importlib
        from game import settings
        importlib.reload(settings)
        if settings.IS_TEST_VERSION:
            game_menu.add_command(label="测试游戏胜利", command=self._test_game_won)  # 添加测试选项
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

    def _reveal_zeros(self, row, col):
        """递归揭示值为 0 的单元格及其周围的单元格"""
        if (row, col) in self.visited:
            return
        self.visited.add((row, col))

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
                if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                    self._reveal_zeros(nr, nc)
        
        #如果已经揭露了，就不用再重新揭露了
        self.revealed_cells += 1
        logging.debug(f"Revealed cells: {self.revealed_cells}")


    def _on_left_click(self, row, col):
        """处理左键点击事件"""
        if self.game_over:
            return

        if self.start_time is None:
            self._start_timer()

        if (row, col) in self.visited:
            logging.debug(f"visited: {self.visited}")
            return
        

        value = self.board.reveal_cell(row, col)
        
        if value == -1:
            self._stop_timer()
            self.buttons[row][col].config(text="💣", bg="red")
            self._game_over()
        elif value == 0:
            self._reveal_zeros(row, col)
        else:
            self.visited.add((row, col))
            self.buttons[row][col].config(text=str(value), state="disabled", bg="lightgrey")
            self.revealed_cells += 1
            logging.debug(f"Revealed cells: {self.revealed_cells}")

        if self.revealed_cells == GRID_ROWS * GRID_COLS - NUM_MINES:
            self._game_won()

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
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                self.buttons[row][col].config(state="disabled")

    def _game_won(self):
        """游戏胜利"""
        self._stop_timer()
        self.game_over = True
        elapsed_time = int(time.time() - self.start_time)
        messagebox.showinfo("胜利", f"恭喜你赢了！用时: {elapsed_time} 秒")
        logging.info("Victory condition met. Game won!")

        if self.difficulty in self.best_times and elapsed_time < self.best_times[self.difficulty]["time"]:
            self.best_times[self.difficulty]["time"] = elapsed_time
            self._record_score(elapsed_time)

    def _record_score(self, elapsed_time):
        """记录玩家成绩"""
        record_window = tk.Toplevel(self.root)
        record_window.title("记录成绩")
        record_window.transient(self.root)  # 设置为模态框
        record_window.grab_set()  # 禁止操作主窗口

        # 创建一个容器框架用于放置标签
        label_frame = tk.Frame(record_window)
        label_frame.grid(row=0, column=0, columnspan=2, pady=10)

        # 将标签放入容器框架中
        tk.Label(label_frame, text=f"已破{self.difficulty}纪录！").pack(side="top", pady=5)
        tk.Label(label_frame, text="请留下尊姓大名!").pack(side="bottom", pady=5)

        name_entry = tk.Entry(record_window)
        name_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        def save_record():
            name = name_entry.get().strip()
            if name:
                self.best_times[self.difficulty]["name"] = name
                self.best_times[self.difficulty]["time"] = elapsed_time
                save_records(self.best_times)  # 确保调用正确的保存函数
                record_window.destroy()
                self._show_records()  # 跳转到扫雷英雄榜界面
            else:
                messagebox.showerror("错误", "请输入有效的名字！")

        
        tk.Button(record_window, text="确定", command=save_record).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        def on_close():
            """提示用户关闭模态框"""
            self.root.bell()  # 发出提示音
            messagebox.showwarning("提示", "请先关闭记录窗口！")

        record_window.protocol("WM_DELETE_WINDOW", on_close)  # 禁止直接关闭窗口
        record_window.wait_window()  # 等待模态框关闭

    def _show_records(self):
        """显示记录界面"""
        records_window = tk.Toplevel(self.root)
        records_window.title("记录")

        # 创建一个容器框架用于放置记录内容
        content_frame = tk.Frame(records_window)
        content_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        tk.Label(content_frame, text="扫雷游戏记录", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(content_frame, text="难度").grid(row=1, column=0, padx=10)
        tk.Label(content_frame, text="玩家").grid(row=1, column=1, padx=10)
        tk.Label(content_frame, text="时间 (秒)").grid(row=1, column=2, padx=10)

        for i, (difficulty, record) in enumerate(self.best_times.items(), start=2):
            tk.Label(content_frame, text=difficulty).grid(row=i, column=0, padx=10)
            tk.Label(content_frame, text=record["name"]).grid(row=i, column=1, padx=10)
            tk.Label(content_frame, text=record["time"]).grid(row=i, column=2, padx=10)

        def reset_scores():
            """重新初始化记录数据"""
            self.best_times = {
                "初级": {"time": 999, "name": "匿名"},
                "中级": {"time": 999, "name": "匿名"},
                "高级": {"time": 999, "name": "匿名"}
            }
            save_records(self.best_times)  # 保存初始化后的记录
            # 刷新页面上的数据
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="扫雷游戏记录", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

            tk.Label(content_frame, text="难度").grid(row=1, column=0, padx=10)
            tk.Label(content_frame, text="玩家").grid(row=1, column=1, padx=10)
            tk.Label(content_frame, text="时间 (秒)").grid(row=1, column=2, padx=10)

            for i, (difficulty, record) in enumerate(self.best_times.items(), start=2):
                tk.Label(content_frame, text=difficulty).grid(row=i, column=0, padx=10)
                tk.Label(content_frame, text=record["name"]).grid(row=i, column=1, padx=10)
                tk.Label(content_frame, text=record["time"]).grid(row=i, column=2, padx=10)

        button_frame = tk.Frame(records_window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        tk.Button(button_frame, text="重新计分", command=reset_scores).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="确定", command=records_window.destroy).grid(row=2, column=1, padx=10, pady=10)


    def _test_game_won(self):
        """测试游戏胜利流程"""
        if self.start_time is None:
            self.start_time = time.time()  # 初始化开始时间
        self.revealed_cells = GRID_ROWS * GRID_COLS - NUM_MINES  # 模拟所有非雷单元格已被揭示
        self._game_won()

    def _restart_game(self):
        """重新开始游戏"""
        self._stop_timer()
        self.board = Board()  # 重置游戏逻辑
        self.start_time = None
        self.game_over = False
        self.remaining_flags = NUM_MINES
        self.revealed_cells = 0
        self.visited=set()
        self.timer_label.config(text="Time: 0s")
        self.flags_label.config(text=f"Flags: {self.remaining_flags}")

        # 重新创建按钮网格
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons[row])):
                self.buttons[row][col].destroy()
        self.buttons = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self._create_widgets()

    def _show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", "扫雷游戏\n作者: 耿耿星河\n版本: 1.0")

    def _set_difficulty(self, difficulty):
        """设置游戏难度"""
        self.difficulty = difficulty
        if difficulty == "初级":
            self._update_settings(9,9, 10)
        elif difficulty == "中级":
            self._update_settings(16,16, 40)
        elif difficulty == "高级":
            self._update_settings(16,30, 99)
        self._restart_game()

    def _custom_difficulty(self):
        """自定义难度设置"""
        custom_window = tk.Toplevel(self.root)
        custom_window.title("自定义难度")

        tk.Label(custom_window, text="网格大小 (行 x 列):").grid(row=0, column=0, padx=5, pady=5)
        rows_entry = tk.Entry(custom_window, width=5)
        rows_entry.grid(row=0, column=1, padx=5, pady=5)
        cols_entry = tk.Entry(custom_window, width=5)
        cols_entry.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(custom_window, text="地雷数量:").grid(row=1, column=0, padx=5, pady=5)
        mines_entry = tk.Entry(custom_window, width=10)
        mines_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        def apply_custom_settings():
            try:
                rows = int(rows_entry.get())
                cols = int(cols_entry.get())
                mines = int(mines_entry.get())
                if rows > 0 and cols > 0 and 0 < mines < rows * cols:
                    self._update_settings(rows, cols, mines)
                    self._restart_game()
                    custom_window.destroy()
                else:
                    tk.messagebox.showerror("错误", "输入的值无效！")
            except ValueError:
                tk.messagebox.showerror("错误", "请输入有效的数字！")

        tk.Button(custom_window, text="应用", command=apply_custom_settings).grid(row=2, column=0, columnspan=3, pady=10)

    def _update_settings(self, rows, cols, mines):
        """更新游戏设置并重新初始化棋盘和按钮网格"""
        global GRID_ROWS, GRID_COLS, NUM_MINES
        GRID_ROWS = rows
        GRID_COLS = cols
        NUM_MINES = mines

        # 更新逻辑棋盘
        self.board.update_board(rows, cols, mines)

        # 重新创建按钮网格
        for row in range(len(self.buttons)):
            for col in range(len(self.buttons[row])):
                self.buttons[row][col].destroy()
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self._create_widgets()  # 重新创建网格按钮

    def run(self):
        """运行游戏"""
        self.root.mainloop()