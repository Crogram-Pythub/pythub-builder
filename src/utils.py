# _*_ coding:utf-8 _*_
# utils functions

import sys
import subprocess
from pathlib import Path
from tkinter import messagebox

def set_window_center(root, width=None, height=None, minsize=True, resize=False):
    """设置窗口宽高及居中"""
    # 获取窗口宽高
    if width is None or height is None:
        # 宽高为 None 时取窗口自身大小
        root.update_idletasks() # 更新
        root.withdraw() # 隐藏重绘
        # root.update() # 获取窗口宽高之前需要先刷新窗口
    if width is None:
        width = root.winfo_width()
    if height is None:
        height = root.winfo_height()

    # 获取屏幕宽高
    w_s = root.winfo_screenwidth()
    h_s = root.winfo_screenheight()

    # 计算 x, y 位置
    x_co = (w_s - width) / 2
    y_co = (h_s - height) / 2

    # 设置窗口宽高和居中定位
    root.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
    # root.geometry(f"{width}x{height}+{x_co}+{y_co}")
    root.deiconify() # 显示
    # 是否设置窗口最小尺寸
    if minsize:
        root.minsize(width, height)
    # 是否可调整大小
    if resize:
        root.resizable(True, True)
    else:
        root.resizable(False, False)


def get_screen_size(root):
    """获取屏幕 宽、高"""
    return root.winfo_screenwidth(), root.winfo_screenheight()


def get_window_size(root):
    """获取窗口 宽、高"""
    root.update()
    return root.winfo_width(), root.winfo_height()

def find_pyinstaller():
    '''根据系统选择命令'''
    if sys.platform == "win32":
        cmd = ["where", "pyinstaller.exe"]
    else:
        cmd = ["which", "pyinstaller"]

    # 执行命令并获取输出
    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True, timeout=5
        )
        paths = result.stdout.strip().split("\n")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    # 验证找到的路径
    for _path in paths:
        path = _path.strip()
        # 处理Windows where命令可能的额外输出
        if sys.platform == "win32" and ":\\" not in path:
            continue
        if Path(path).is_file():
            return Path(path).absolute()

def app_quit(root):
    '''退出'''
    if messagebox.askyesno('提示', '确定退出？') is True:
        root.quit()
