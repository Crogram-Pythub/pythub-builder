# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from multiprocessing import Process, freeze_support

from view import View

def run():
    app = tk.Tk()
    app.title("Pythub Builder 1.1.0")

    # 配置根窗口网格布局
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    # 样式配置
    # app_style = ttk.Style()
    # app_style.configure("TButton", padding=6)
    # app_style.configure("TLabel", padding=3)
    # app_style.configure("TEntry", padding=3)

    View(app)
    # set_window_center(app)
    app.mainloop()


if __name__ == "__main__":
    freeze_support()
    run()
    # Process(target=run).start()
