import sys
import subprocess
import os

def build(mode):
    assert mode in ["test", "release"], "Mode must be 'test' or 'release'"
    settings_path = "game/settings.py"
    with open(settings_path, "r", encoding="utf-8") as file:  # 指定编码为 utf-8
        lines = file.readlines()

    with open(settings_path, "w", encoding="utf-8") as file:  # 指定编码为 utf-8
        for line in lines:
            if line.startswith("IS_TEST_VERSION"):
                file.write(f"IS_TEST_VERSION = {mode == 'test'}\n")
            else:
                file.write(line)

    # 设置输出目录
    output_dir = os.path.join("dist", mode)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Building {mode} version...")
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--icon=assets/images/icon.ico",
        f"--distpath={output_dir}",  # 指定输出目录
        "main.py"
    ])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build.py [test|release]")
        sys.exit(1)
    build(sys.argv[1])