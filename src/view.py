# -*- coding: utf-8 -*-

import pathlib
from threading import Thread
from tkinter import (
    IntVar,
    StringVar,
)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
# from PyInstaller.__main__ import run as pirun
from functools import partial

from utils import set_window_center, find_pyinstaller, app_quit


class View(object):

    def __init__(self, master=None):
        set_window_center(master, 700, 800, resize=True)
        self.root = master
        self.status_build = False
        self.entry_value_list = list()
        # 日志
        self.log_text = None
        # 状态栏
        self.label_status = None
        # 按钮：打包
        self.btn_build = None
        # 定义变量，并初始化
        self.cfg_onefile = IntVar(value=1)
        self.cfg_onedir = IntVar(value=0)
        self.cfg_noconsole = IntVar(value=1)
        self.cfg_clean = IntVar(value=1)
        self.cfg_upx = IntVar(value=1)  # UPX 默认开启
        self.cfg_rename = IntVar()
        self.cfg_exe_name = StringVar()
        # 自定义配置文件
        self.cfg_specfile = StringVar(value="build.spec")

        self.init_view()

    def init_view(self):
        """基本框架"""
        self.frm_main = tk.LabelFrame(self.root, borderwidth=0)
        self.frm_main.pack(side="left", fill="both", expand=True)
        # self.frm_main.grid(row=0, column=0, sticky="ew")
        # self.frm_main.grid_rowconfigure(0, weight=1)
        # self.frm_main.grid_columnconfigure(0, weight=1)

        # self.frm_advance = tk.LabelFrame(self.root, text='高级选项')
        # self.frm_advance.pack(expand='yes', side='right', fill='both', padx=15, pady=10)
        # self.frm_2 = tk.LabelFrame(self.frm_advance, text='高级配置', width=300)
        # self.frm_2.pack(expand='yes', side='top', fill='both', padx=15, pady=10)

        self.frm_project = tk.LabelFrame(self.frm_main, text="项目信息")
        self.frm_operate = tk.Frame(self.frm_main)
        self.frm_config = tk.LabelFrame(self.frm_operate, text="配置信息")
        self.frm_command = tk.LabelFrame(self.frm_operate, text="操作")
        self.frm_logs = tk.LabelFrame(self.frm_main, text="日志输出", padx=10, pady=10)
        self.frm_status = tk.LabelFrame(self.frm_main, text="状态")

        self.frm_project.pack(side="top", fill="x", padx=15, pady=10)
        self.frm_operate.pack(side="top", fill="x", padx=15, pady=10)

        self.frm_config.grid(row=0, column=0, sticky="nsew", padx=2)
        self.frm_config.grid_columnconfigure(0, weight=1)
        self.frm_config.grid_rowconfigure(0, weight=1)
        self.frm_command.grid(row=0, column=1, sticky="ns", padx=2)
        # self.frm_command.grid_columnconfigure(1, weight=1)
        # self.frm_command.grid_rowconfigure(0, weight=1)

        self.frm_logs.pack(side="top", fill="both", padx=15, pady=10, expand=True)
        self.frm_logs.grid_rowconfigure(0, weight=1)
        self.frm_logs.grid_columnconfigure(0, weight=1)
        self.frm_status.pack(side="bottom", fill="x", padx=15, pady=10)

        self.view_project()
        self.view_config()
        self.view_operate()
        self.view_logs()
        self.view_status()

    def view_project(self):
        """项目配置"""
        labels = ["主程序入口文件", "工作目录", "打包输出路径", "程序图标", "版本信息文件"]
        for index, label_text in enumerate(labels):
            temp_strvar = StringVar()
            temp_label = tk.Label(self.frm_project, text=label_text)
            temp_entry = tk.Entry(self.frm_project, textvariable=temp_strvar, width=48)
            self.entry_value_list.append(temp_strvar)
            temp_label.grid(row=index % 5, column=0, padx=5, pady=5, sticky="w")
            temp_entry.grid(row=index % 5, column=1, padx=5, pady=5, sticky="we")
            temp_entry.grid_rowconfigure(0, weight=1)
            temp_entry.grid_columnconfigure(0, weight=1)

        btn_main_path = tk.Button(
            self.frm_project, text="选择文件", command=self.fn_select_main
        )
        btn_work_path = tk.Button(
            self.frm_project, text="选择路径", command=self.fn_work_path
        )
        btn_dist_path = tk.Button(
            self.frm_project, text="选择路径", command=self.fn_dist_path
        )
        btn_ico_path = tk.Button(
            self.frm_project, text="选择图标", command=self.fn_icon_path
        )
        btn_vers_path = tk.Button(
            self.frm_project, text="选择文件", command=self.fn_vers_path
        )

        btn_main_path.grid(row=0, column=2, padx=5, pady=5, sticky="we")
        btn_work_path.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        btn_dist_path.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        btn_ico_path.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        btn_vers_path.grid(row=4, column=2, padx=5, pady=5, sticky="e")

    def view_config(self):
        """配置选项"""
        # 子配置框架
        self.frm_config_base = tk.LabelFrame(
            self.frm_config, text="基本", borderwidth=0
        )
        self.frm_config_base.pack(fill="x", padx=10, pady=5, ipady=5)
        self.frm_config_exe = tk.LabelFrame(
            self.frm_config, text="生成执行文件类型", borderwidth=0
        )
        self.frm_config_exe.pack(fill="x", padx=10, pady=5, ipady=5)
        self.frm_config_other = tk.LabelFrame(
            self.frm_config, text="其它", borderwidth=0
        )
        self.frm_config_other.pack(fill="x", padx=10, pady=5, ipady=5)
        self.frm_config_spec = tk.LabelFrame(
            self.frm_config, text="配置文件", borderwidth=0
        )
        self.frm_config_spec.pack(fill="x", padx=10, pady=5, ipady=5)

        # 定义按钮
        self.btn_noconsole = tk.Checkbutton(
            self.frm_config_base, text="关闭控制台", variable=self.cfg_noconsole
        )
        self.btn_clean = tk.Checkbutton(
            self.frm_config_base, text="构建前清理", variable=self.cfg_clean
        )
        self.btn_upx = tk.Checkbutton(
            self.frm_config_base, text="UPX压缩", variable=self.cfg_upx
        )
        self.btn_isonefile = tk.Checkbutton(
            self.frm_config_exe, text="独立执行文件", variable=self.cfg_onefile
        )
        self.btn_isonedir = tk.Checkbutton(
            self.frm_config_exe, text="文件夹包含", variable=self.cfg_onedir
        )
        self.btn_rename = tk.Checkbutton(
            self.frm_config_other, text="修改执行文件名", variable=self.cfg_rename
        )
        self.entry_rename = tk.Entry(
            self.frm_config_other, textvariable=self.cfg_exe_name
        )

        # self.btn_rename = tk.Checkbutton(self.frm_config_spec, text='生成配置文件', variable=self.cfg_specfile)
        self.entry_specfile = tk.Entry(
            self.frm_config_spec, textvariable=self.cfg_specfile
        )

        # 放置按钮
        self.btn_isonefile.pack(side="left", fill="x")
        self.btn_isonedir.pack(side="left", fill="x")
        self.btn_noconsole.pack(side="left", fill="x")
        self.btn_clean.pack(side="left", fill="x")
        self.btn_upx.pack(side="left", fill="x")
        self.btn_rename.pack(side="left", fill="x")
        self.entry_rename.pack(fill="x")
        self.entry_specfile.pack(fill="x")

        # 变量自动切换操作
        self.cfg_onefile.trace("w", self.cfg_onefile_trace)
        self.cfg_onedir.trace("w", self.cfg_onedir_trace)

    def cfg_onefile_trace(self, *args):
        """cfg_onefile 与 cfg_onedir 可以同时不选，但不能同时选中，选中独立执行文件时不能选中文件夹包"""
        if self.cfg_onefile.get() == 1:
            self.cfg_onedir.set(0)

    def cfg_onedir_trace(self, *args):
        """cfg_onefile 与 cfg_onedir 可以同时不选，但不能同时选中，选中文件夹包含时不能选中独立执行文件"""
        if self.cfg_onedir.get() == 1:
            self.cfg_onefile.set(0)

    def view_operate(self):
        """操作命令"""
        # 定义按钮
        self.btn_build = tk.Button(
            self.frm_command, text="构建生成", command=self.fn_build
        )
        btn_reset = tk.Button(self.frm_command, text="重置表单", command=self.fn_reset)
        btn_clear = tk.Button(self.frm_command, text="清理文件", command=self.fn_clear)
        btn_advance = tk.Button(
            self.frm_command, text="高级选项", command=self.fn_toggle_advance
        )
        btn_about = tk.Button(
            self.frm_command, text="关于应用", command=self.fn_toggle_about
        )
        btn_quit = tk.Button(
            self.frm_command, text="退出应用", command=partial(app_quit, self.root)
        )

        # 放置按钮
        self.btn_build.pack(fill="x", padx=15)
        btn_reset.pack(fill="x", padx=15)
        btn_clear.pack(fill="x", padx=15)
        btn_advance.pack(fill="x", padx=15)
        btn_about.pack(fill="x", padx=15)
        btn_quit.pack(fill="x", padx=15, side="bottom", pady=10)

    def view_logs(self):
        """日志"""
        self.log_text = tk.Text(
            self.frm_logs,
            wrap=tk.WORD,
            font=("Consolas", 12),
            highlightthickness=0,
            height=8,
        )
        scrollbar = ttk.Scrollbar(
            self.frm_logs, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="nsew")

    def view_status(self):
        """状态栏"""
        self.label_status = tk.Label(self.frm_status, text="待命")
        self.label_status.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    def fn_build(self):
        """生成可执行文件"""
        if len(self.entry_value_list[0].get()) == 0:
            self.label_status["text"] = "请选择要打包的 Python 脚本"
            self.root.after(
                0, messagebox.showerror, "错误", "请选择要打包的 Python 脚本！"
            )
            return
        if not pathlib.Path(self.entry_value_list[0].get()).exists():
            self.label_status["text"] = "选定的 Python 脚本不存在！"
            self.root.after(
                0, messagebox.showerror, "错误", "指定的 Python 脚本不存在！"
            )
            return

        if not self.status_build:
            # 启动后台线程执行打包命令
            # thread_build = Thread(target=self.fn_build_thread)
            # thread_build.setDaemon(True)
            # thread_build.start()
            Thread(target=self.fn_build_thread, daemon=True).start()
        else:
            self.label_status["text"] = "正在打包中，请稍后再操作！"
            self.root.after(
                0, messagebox.showerror, "错误", "正在打包中，请稍后再操作！"
            )

    def fn_build_thread(self):
        """执行打包命令"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("准备打包")
        cmd = self.fn_build_cmd()
        self.log_message("组装命令: " + " ".join(cmd))
        self.status_build = True
        self.btn_build.config(state=tk.DISABLED)
        self.label_status["text"] = "正在打包，请稍等。。。"
        try:
            process = subprocess.Popen(
                " ".join(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding="utf-8",
                errors="replace",
            )

            # 实时读取输出
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self.root.after(0, self.log_message, output.strip())

            # 处理返回结果
            return_code = process.poll()
            if return_code == 0:
                self.status_build = False
                self.label_status["text"] = "打包完成"
                self.root.after(0, self.log_message, "打包完成！")
                self.root.after(0, messagebox.showinfo, "完成", "打包操作成功完成！")
            else:
                error_msg = f"打包失败，错误码：{return_code}"
                self.status_build = False
                self.label_status["text"] = error_msg
                self.root.after(0, self.log_message, error_msg)
                self.root.after(0, messagebox.showerror, "错误", error_msg)

        except Exception as e:
            error_msg = f"打包失败，发生未预期错误：{str(e)}"
            self.status_build = False
            self.label_status["text"] = error_msg
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, messagebox.showerror, "异常错误", error_msg)
        finally:
            self.status_build = False
            self.root.after(0, self.btn_build.config, {"state": tk.NORMAL})

    def fn_clear(self):
        """清理生成文件"""
        self.log_text.delete(1.0, tk.END)

    def fn_reset(self):
        """重置表单内容"""
        for i in range(5):
            self.entry_value_list[i].set("")

        self.cfg_onefile.set(1)
        self.cfg_noconsole.set(1)
        self.cfg_clean.set(1)
        self.cfg_upx.set(1)
        self.cfg_rename.set(0)
        self.cfg_exe_name.set("")
        self.cfg_specfile.set("build.spec")

    def fn_toggle_advance(self):
        """切换高级选项界面"""
        messagebox.showinfo("提示", "高级选项功能暂未开发！")
        # if self.frm_advance.winfo_ismapped():
        #     # self.root.width = self.root.winfo_width() - 400
        #     # set_window_center(self.root, width=(self.root.winfo_width() - 400))
        #     self.frm_advance.pack_forget()
        # else:
        #     # self.root.width = self.root.winfo_width() + 400
        #     # set_window_center(self.root, width=(self.root.winfo_width() + 400))
        #     # self.frm_advance.pack(expand='yes',
        #     #                       side='right',
        #     #                       fill='both',
        #     #                       padx=15,
        #     #                       pady=10)
        #     self.frm_advance.grid(row=0, column=1, sticky="nsew")

    def fn_select_main(self):
        """选择源文件"""
        types = (
            ("Python文件", "*.py"),
            ("PYC文件", "*.pyc"),
            ("SPEC文件", "*.spec"),
            ("所有文件", "*.*"),
        )
        path = filedialog.askopenfilename(filetypes=types)
        if not path:
            return
        _path = pathlib.Path(path).parent
        # 主文件
        self.entry_value_list[0].set(path)
        # 工作目录
        self.entry_value_list[1].set(_path.joinpath("build"))
        # dist目录
        self.entry_value_list[2].set(_path.joinpath("dist"))

    def fn_work_path(self):
        """选择工作目录"""
        path = filedialog.askdirectory()
        if not path:
            return
        self.entry_value_list[1].set(path)

    def fn_dist_path(self):
        """选择生成文件目录"""
        path = filedialog.askdirectory()
        if not path:
            return
        self.entry_value_list[2].set(path)

    def fn_icon_path(self):
        """选择图标文件"""
        types = (("ICO图标", "*.ico"), ("ICNS图标", "*.icns"), ("所有文件", "*.*"))
        path = filedialog.askopenfilename(filetypes=types)
        if not path:
            return
        self.entry_value_list[3].set(path)

    def fn_vers_path(self):
        """选择图标文件"""
        types = (("资源文件", "*.rc *.txt"), ("所有文件", "*.*"))
        path = filedialog.askopenfilename(filetypes=types)
        if not path:
            return
        self.entry_value_list[4].set(path)

    def fn_detect_pyinstaller(self):
        '''查找 PyInstaller：'''
        pyinstaller = 'pyinstaller'
        try:
            path = find_pyinstaller()
            if path is not None:
                pyinstaller = str(path.absolute())
                self.log_message(f"已找到 PyInstaller: {pyinstaller}")
                # 构建命令示例
                # command = [pyinstaller, "--version"]
                # self.log_message(f"PyInstaller 版本: {subprocess.run(command, check=True)}")
        except Exception as e:
            error_msg = f"未找到 PyInstaller: {str(e)}"
            self.status_build = False
            self.root.after(0, self.log_message, error_msg)
            self.root.after(0, messagebox.showerror, "异常错误", error_msg)
            self.log_message(f'尝试使用 {pyinstaller} 命令')

        return pyinstaller

        # try:
        #     process = subprocess.Popen(
        #         " ".join(cmd),
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.STDOUT,
        #         shell=True,
        #         encoding="utf-8",
        #         errors="replace",
        #     )

        #     # 实时读取输出
        #     while True:
        #         output = process.stdout.readline()
        #         if output == "" and process.poll() is not None:
        #             break
        #         if output:
        #             self.root.after(0, self.log_message, output.strip())


    def fn_build_cmd(self, cli=True):
        """组装命令"""
        pyinstaller = self.fn_detect_pyinstaller()
        cmds = [pyinstaller]
        # if cli is True:
        #     # 使用系统命令行
        #     cmds.append(pyinstaller)

        if len(self.entry_value_list[0].get()) > 0:
            cmds.append(self.entry_value_list[0].get())
        else:
            return cmds

        cmds.append("--windowed")
        cmds.append("-y")
        cmds.append("--noconfirm")
        # cmds.append('--filenames=build.spec')

        if self.cfg_onefile.get() == 1:
            cmds.append("--onefile")
        elif self.cfg_onedir.get() == 1:
            cmds.append("--onedir")

        if self.cfg_clean.get() == 1:
            cmds.append("--clean")
            cmds.append("--noconfirm")

        if self.cfg_upx.get() == 0:
            cmds.append("--noupx")

        if self.cfg_noconsole.get() == 1:
            cmds.append("--noconsole")

        if len(self.entry_value_list[1].get()) > 0:
            cmds.append("--workpath=" + self.entry_value_list[1].get())
            cmds.append("--specpath=" + self.entry_value_list[1].get())

        if len(self.entry_value_list[2].get()) > 0:
            cmds.append("--distpath=" + self.entry_value_list[2].get())

        if len(self.entry_value_list[3].get()) > 0:
            if not pathlib.Path(self.entry_value_list[3].get()).exists():
                messagebox.showerror("错误", "图标文件不存在！")
                return
            cmds.append("--icon=" + self.entry_value_list[3].get())

        # 添加版本信息
        if len(self.entry_value_list[4].get()) > 0:
            if not pathlib.Path(self.entry_value_list[4].get()).exists():
                messagebox.showerror("错误", "版本信息文件不存在！")
                return
            cmds.append("--version-file=" + self.entry_value_list[4].get())

        if self.cfg_rename.get() == 1:
            if len(self.cfg_exe_name.get()) > 0:
                cmds.append("--name=" + self.cfg_exe_name.get())

        if len(self.cfg_specfile.get()) > 0:
            # cmds.extend(["--specfile", f'"{self.cfg_specfile.get()}"'])
            pass

        return cmds

    def log_message(self, message):
        """在日志区域显示消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def fn_toggle_about(self):
        """关于应用"""
        messagebox.showinfo("关于应用", "关于应用\nPythub Builder 1.0")


if __name__ == "__main__":
    root = tk.Tk()
    View(root)
    root.mainloop()
