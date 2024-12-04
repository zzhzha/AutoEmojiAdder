#Python 版本: 3.8.10

from ui import Win as MainWin
# 导入窗口控制器
from control import Controller as MainUIController
# from tkinter import *
# from tkinter.ttk import *
# from tkinter import Scale

# 将窗口控制器 传递给UI
app = MainWin(MainUIController())
if __name__ == "__main__":
    # 启动
    app.mainloop()
