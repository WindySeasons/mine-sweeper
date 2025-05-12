## 扫雷游戏

### 项目简介
这是一个基于 Python 和 Tkinter 的扫雷游戏，支持多种难度模式（初级、中级、高级、自定义），并提供计时功能、标记功能以及记录功能。

### 功能特性
- **多种难度模式**：
  - 初级：9x9 网格，10 个地雷。
  - 中级：16x16 网格，40 个地雷。
  - 高级：30x16 网格，99 个地雷。
  - 自定义：用户可自由设置网格大小和地雷数量。
- **计时功能**：记录玩家完成游戏所用时间。
- **标记功能**：右键标记地雷，防止误操作。
- **记录功能**：保存玩家的最佳成绩，并显示扫雷英雄榜。

### 安装依赖
在运行游戏之前，请确保已安装所需的依赖库。运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

### 运行游戏
使用以下命令运行游戏：

```bash
python main.py
```

### 打包说明
使用以下命令生成可执行文件：

```bash
pyinstaller --onefile --windowed --icon=assets/images/icon.ico main.py
```

#### 参数说明
- `--onefile`：将所有文件打包成一个可执行文件。
- `--windowed`：隐藏控制台窗口（适用于 GUI 应用）。
- `--icon`：指定图标文件。

生成的可执行文件会出现在 `dist/` 文件夹中。

### 测试
本项目包含单元测试，测试文件位于 `tests/` 目录下。运行以下命令执行测试：

```bash
python -m unittest discover -s ./tests -p "test_*.py"
```

### 文件结构
```
├── main.py               # 主程序入口
├── game/                 # 游戏逻辑模块
│   ├── board.py          # 游戏核心逻辑
│   ├── records.py        # 记录管理
│   ├── settings.py       # 游戏配置
│   ├── ui.py             # 用户界面
├── tests/                # 测试文件
│   ├── test_board.py     # 测试游戏核心逻辑
│   ├── test_records.py   # 测试记录管理
│   ├── test_ui.py        # 测试用户界面
├── assets/               # 静态资源
│   ├── images/           # 图标资源
│   ├── sounds/           # 音效资源
├── requirements.txt      # 依赖文件
├── README.md             # 项目说明
```

### 扫雷英雄榜
游戏会记录玩家在不同难度下的最佳成绩，记录存储在 `records.json` 文件中。玩家可以通过菜单查看扫雷英雄榜。

### 贡献
如果你对本项目有任何建议或改进，欢迎提交 Pull Request 或 Issue！