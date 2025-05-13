import sys
import importlib

if not getattr(sys, "frozen", False):  # 检查是否在打包环境中
    # 动态修改 settings.py 中的 IS_TEST_VERSION
    settings_path = "game/settings.py"
    with open(settings_path, "r", encoding="utf-8") as file:  # 指定编码为 utf-8
        lines = file.readlines()

    with open(settings_path, "w", encoding="utf-8") as file:  # 指定编码为 utf-8
        for line in lines:
            if line.startswith("IS_TEST_VERSION"):
                file.write(f"IS_TEST_VERSION = {sys.argv[1] == '--test'}\n")
            else:
                file.write(line)

    # 强制重新加载 settings 模块
    from game import settings
    importlib.reload(settings)
else:
    # 在打包环境中直接导入 settings
    from game import settings

if __name__ == "__main__":
    print(f"Running in {'test' if settings.IS_TEST_VERSION else 'release'} mode")
    # 启动游戏
    from game.ui import MinesweeperUI
    MinesweeperUI().run()