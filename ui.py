from tkinter import *
from tkinter.ttk import *
from tkinter import Scale


class TableFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tree = self.create_table()
        self.xscroll, self.yscroll = self.create_scrollbars(self.tree)

    def create_table(self):
        tree = Treeview(self, columns="path")
        tree.column("#0", anchor=CENTER)
        tree.column("path", anchor=CENTER)
        tree.heading('#0', text='name')
        tree.heading('path', text='path')
        return tree

    def create_scrollbars(self, tree):
        xscroll = Scrollbar(self, orient=HORIZONTAL)
        yscroll = Scrollbar(self, orient=VERTICAL)
        xscroll.config(command=tree.xview)
        yscroll.config(command=tree.yview)
        return xscroll, yscroll

    def pack_(self, cnf={}, **kw):
        self.pack(cnf, **kw)
        self.xscroll.pack(side=BOTTOM, fill=X)
        self.yscroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=1)


class ImageConfigLabelFrame(Labelframe):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.max_image_length_config_scale = self.create_max_image_length_config_scale()
        self.inquire_enlarge_pic_config_checkbutton = self.create_inquire_enlarge_pic_config_checkbutton()

    def create_max_image_length_config_scale(self):
        scale = Scale(self, from_=1, to=1024, orient=HORIZONTAL, label="图片边长（1~1024）")
        return scale

    def create_inquire_enlarge_pic_config_checkbutton(self):
        checkbutton = Checkbutton(self, text="是否放大小于所设定最长图片边长的图片", variable=IntVar(), onvalue=1,
                                  offvalue=0)
        return checkbutton

    def pack_(self, cnf={}, **kw):
        self.pack(cnf, **kw)
        self.max_image_length_config_scale.pack(side=TOP, fill=X, padx=6, pady=3)
        self.inquire_enlarge_pic_config_checkbutton.pack(side=TOP, expand=1, padx=6, pady=3)

class MainFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.start_button = self.create_start_button()
        self.select_emoji_folder_button = self.create_select_emoji_folder_button()
        self.empty_frame = self.create_empty_frame()
        self.image_config_frame = self.create_image_config_frame()

    def create_start_button(self):
        button = Button(self, text="开始")
        return button

    def create_select_emoji_folder_button(self):
        button = Button(self, text="选择表情包文件夹")
        return button

    def create_empty_frame(self):
        frame = Frame(self)
        return frame

    def create_image_config_frame(self):
        image_config_frame = ImageConfigLabelFrame(self,text="图片配置")
        return image_config_frame

    def pack_(self, cnf={}, **kw):
        self.pack(cnf, **kw)
        self.start_button.pack(side=TOP, fill='none', padx=8, pady=8,ipadx=5, ipady=3)
        self.select_emoji_folder_button.pack(side=TOP, fill='none', expand=1, padx=8, pady=3,ipadx=5, ipady=3)
        self.empty_frame.pack(side=TOP, fill=BOTH, expand=1, padx=8, pady=3)
        self.image_config_frame.pack_(side=BOTTOM, fill=BOTH, expand=1, padx=8, pady=6)


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.table_frame = self.__table_frame()
        self.main_frame = self.__main_frame()

    def __win(self):
        self.title("Tkinter")
        # self.geometry("800x600")
        # self.resizable(width=False, height=False)

    def __table_frame(self):
        table_frame = TableFrame(self)
        table_frame.pack_(side=LEFT, fill=BOTH, expand=1)
        return table_frame

    def __main_frame(self):
        main_frame = MainFrame(self)
        main_frame.pack_(side=LEFT, fill=BOTH, expand=1)
        return main_frame


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        # self.ctl.init(self)
        # self.tk_check_button_enlarge_pic_checkbutton.config(variable=self.ctl.ENLARGE_STATE)

    def __event_bind(self):
        pass
    #     self.tk_table_table.bind('<Double-Button-1>', self.ctl.show_image)
    #     self.tk_table_table.bind('<Delete>', self.ctl.multi_delete_image)
    #
    #     self.tk_button_start_button.bind('<Button-1>', self.ctl.start_add_image)
    #     self.tk_button_select_image_folder_button.bind('<Button-1>', self.ctl.select_image_folder)
    #     self.tk_scale_max_length_scale.bind('<B1-Motion>', self.ctl.set_max_length)

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
