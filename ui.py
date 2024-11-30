from tkinter import *
from tkinter.ttk import *
from tkinter import Scale

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_table_table = self.__tk_table_table(self)
        self.tk_frame_container = self.__tk_frame_container(self)
        self.tk_frame_start_frame = self.__tk_frame_start_frame(self.tk_frame_container)
        self.tk_button_start_button = self.__tk_button_start_button(self.tk_frame_start_frame)
        self.tk_frame_select_image_folder_frame = self.__tk_frame_select_image_folder_frame(self.tk_frame_container)
        self.tk_button_select_image_folder_button = self.__tk_button_select_image_folder_button(
            self.tk_frame_select_image_folder_frame)


        self.tk_frame_input_max_length_frame = self.__tk_frame_input_max_length_frame(self.tk_frame_container)
        self.tk_label_tip_max_length_label = self.__tk_label_tip_max_length_label(self.tk_frame_input_max_length_frame)
        self.tk_scale_max_length_scale = self.__tk_scale_max_length_scale(self.tk_frame_input_max_length_frame)
        self.tk_label_show_limits_label = self.__tk_label_show_limits_label(self.tk_frame_input_max_length_frame)
        self.tk_frame_enlarge_pic_frame = self.__tk_frame_enlarge_pic_frame(self.tk_frame_container)
        self.tk_check_button_enlarge_pic_checkbutton = self.__tk_check_button_enlarge_pic_checkbutton(
            self.tk_frame_enlarge_pic_frame)

    def __win(self):
        self.title("Tkinter布局助手")
        # 设置窗口大小、居中
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_table_table(self, parent):
        # 表头字段 表头宽度
        columns = {"name": 79, "path": 319}
        tk_table = Treeview(parent, show="headings", columns=list(columns), )
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        tk_table.place(x=0, y=0, width=400, height=500)
        self.create_bar(parent, tk_table, True, True, 0, 0, 400, 500, 600, 500)
        return tk_table

    def __tk_frame_container(self, parent):
        frame = Frame(parent, )
        frame.place(x=400, y=0, width=200, height=500)
        return frame

    def __tk_frame_start_frame(self, parent):
        frame = Frame(parent, )
        frame.place(x=0, y=0, width=200, height=60)
        return frame

    def __tk_button_start_button(self, parent):
        btn = Button(parent, text="开始添加", takefocus=False, )
        btn.place(x=50, y=15, width=100, height=30)
        return btn

    def __tk_frame_select_image_folder_frame(self, parent):
        frame = Frame(parent, )
        frame.place(x=0, y=60, width=200, height=100)
        return frame

    def __tk_button_select_image_folder_button(self, parent):
        btn = Button(parent, text="选择图片文件夹", takefocus=False, )
        btn.place(x=50, y=35, width=100, height=30)
        return btn

    def __tk_frame_select_convert_output_folder_frame(self, parent):
        frame = Frame(parent, )
        frame.place(x=0, y=160, width=200, height=100)
        return frame


    def __tk_frame_input_max_length_frame(self, parent):
        frame = Frame(parent, )
        frame.place(x=0, y=260, width=200, height=100)
        return frame

    def __tk_label_tip_max_length_label(self, parent):
        label = Label(parent, text="最长边长度", anchor="center", )
        label.place(x=0, y=20, width=75, height=30)
        return label

    def __tk_scale_max_length_scale(self, parent):
        scale = Scale(parent, orient=HORIZONTAL, from_=1, to=1024)
        scale.place(x=80, y=37, width=120, height=50)
        return scale

    def __tk_label_show_limits_label(self, parent):
        label = Label(parent, text="（1-1024）", anchor="center", )
        label.place(x=0, y=53, width=75, height=30)
        return label

    def __tk_frame_enlarge_pic_frame(self, parent):
        frame = Frame(parent, )
        frame.place(x=0, y=360, width=200, height=140)
        return frame

    def __tk_check_button_enlarge_pic_checkbutton(self, parent):
        cb = Checkbutton(parent, text="是否放大小图片",)
        cb.place(x=41, y=55, width=118, height=30)
        return cb


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
        self.tk_check_button_enlarge_pic_checkbutton.config(variable=self.ctl.ENLARGE_STATE)


    def __event_bind(self):
        self.tk_table_table.bind('<Double-Button-1>', self.ctl.show_image)
        self.tk_table_table.bind('<Delete>', self.ctl.multi_delete_image)

        self.tk_button_start_button.bind('<Button-1>', self.ctl.start_add_image)
        self.tk_button_select_image_folder_button.bind('<Button-1>', self.ctl.select_image_folder)
        self.tk_scale_max_length_scale.bind('<B1-Motion>', self.ctl.set_max_length)


    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
