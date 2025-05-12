## 打包说明

使用以下命令生成可执行文件：

```bash
pyinstaller --onefile --windowed --icon=assets/images/icon.ico main.py
```

### 参数说明
- `--onefile`：将所有文件打包成一个可执行文件。
- `--windowed`：隐藏控制台窗口（适用于 GUI 应用）。
- `--icon`：指定图标文件。

生成的可执行文件会出现在 `dist/` 文件夹中。