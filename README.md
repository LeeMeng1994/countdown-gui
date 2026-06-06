# Countdown GUI

一个基于 Python Tkinter 的桌面倒数日应用，图形化界面更直观。

## 功能特性

- **添加事件**：输入事件名称和日期
- **实时显示**：自动计算并显示剩余天数
- **删除事件**：右键或按钮删除不需要的事件
- **数据持久化**：配置保存在 APPDATA 目录

## 运行方式

```bash
python countdown.py
```

## 打包

```bash
pip install pyinstaller
pyinstaller countdown-gui.spec
```

## 技术栈

- Python 3.12
- Tkinter

## 作者

萌哥