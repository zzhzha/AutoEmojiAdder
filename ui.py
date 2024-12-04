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
        tree.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        xscroll.config(command=tree.xview)
        yscroll.config(command=tree.yview)
        return xscroll, yscroll

    def pack_children(self):
        self.xscroll.pack(side=BOTTOM, fill=X)
        self.yscroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=1)

    def pack(self, cnf={}, **kw):
        super().pack(cnf, **kw)
        self.pack_children()

    def grid(self, cnf={}, **kw):
        super().grid(cnf, **kw)
        self.pack_children()


class IntroductionFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.profile_photo_label = self.create_profile_photo_label()
        self.about_text = self.create_about_text()

    def create_profile_photo_label(self):
        photo = PhotoImage(file="profile.gif")
        label = Label(self, image=photo)
        label.image = photo
        return label

    def create_about_text(self):
        text = """
        这是一个基于 Python 的表情包制作工具。
        你可以选择表情包文件夹，然后将图片按照指定尺寸进行缩放，并将图片名和路径写入表格。
        最后，你可以将表格中的图片拖拽到指定位置，并将其转换为 emoji 表情。
        """
        text_ = Text(self, wrap=WORD, width=30)
        text_.insert(END, text)
        return text_

    def pack_children(self):
        self.profile_photo_label.pack(side=TOP, fill=BOTH, padx=8, pady=3)
        self.about_text.pack(side=TOP, fill=BOTH, expand=1, padx=8, pady=3)

    def pack(self, cnf={}, **kw):
        super().pack(cnf, **kw)
        self.pack_children()

    def grid(self, cnf={}, **kw):
        super().grid(cnf, **kw)
        self.pack_children()


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

    def pack(self, cnf={}, **kw):
        super().pack(cnf, **kw)
        self.max_image_length_config_scale.pack(side=TOP, fill=X, padx=6, pady=3)
        self.inquire_enlarge_pic_config_checkbutton.pack(side=TOP, expand=1, padx=6, pady=3)

    def grid(self, cnf={}, **kw):
        super().grid(cnf, **kw)
        self.max_image_length_config_scale.pack(side=TOP, fill=X, padx=6, pady=3)
        self.inquire_enlarge_pic_config_checkbutton.pack(side=TOP, expand=1, padx=6, pady=3)


class ButtonsFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.start_button = self.create_start_button()
        self.select_emoji_folder_button = self.create_select_emoji_folder_button()

    def create_start_button(self):
        button = Button(self, text="开始")
        return button

    def create_select_emoji_folder_button(self):
        button = Button(self, text="选择表情包文件夹")
        return button

    def pack_children(self):
        self.start_button.pack(side=LEFT, padx=8, pady=3, ipadx=5, ipady=3, expand=1)
        self.select_emoji_folder_button.pack(side=LEFT, padx=8, pady=3, ipadx=5, ipady=3, expand=1)

    def pack(self, cnf={}, **kw):
        super().pack(cnf, **kw)
        self.pack_children()

    def grid(self, cnf={}, **kw):
        super().grid(cnf, **kw)
        self.pack_children()


class MainFunctionFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.buttons_frame = self.create_buttons_frame()
        self.image_config_frame = self.create_image_config_frame()

    def create_image_config_frame(self):
        image_config_frame = ImageConfigLabelFrame(self, text="图片配置")
        return image_config_frame

    def pack_children(self):
        # 貌似grid布局不支持pack布局的子组件，不能自动扩展，所以只能用pack布局
        self.buttons_frame.pack(side=TOP, fill=None, padx=8, pady=3, expand=1)
        self.image_config_frame.pack(side=TOP, fill=None, padx=8, pady=3, expand=1)
        # self.start_button.grid(row=0, column=0, padx=8, pady=3, ipadx=5, ipady=3, sticky=N + W + S + E)
        # self.select_emoji_folder_button.grid(row=0, column=1, padx=8, pady=3, ipadx=5, ipady=3, sticky=N + W + S + E)
        # self.image_config_frame.grid(row=1, column=0, padx=8, pady=3, columnspan=2, sticky=N + W + S + E)

    def pack(self, cnf={}, **kw):
        super().pack(cnf, **kw)
        self.pack_children()

    def grid(self, cnf={}, **kw):
        super().grid(cnf, **kw)
        self.pack_children()

    def create_buttons_frame(self):
        buttons_frame = ButtonsFrame(self)
        return buttons_frame


class ExceptTableFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.introduction_frame = self.create_introduction_frame()
        self.main_function_frame = self.create_main_function_frame()

    def create_introduction_frame(self):
        introduction_frame = IntroductionFrame(self)
        return introduction_frame

    def create_main_function_frame(self):
        main_function_frame = MainFunctionFrame(self)
        return main_function_frame

    def pack_children(self):
        self.introduction_frame.pack(side=TOP, fill=Y, expand=1)
        self.main_function_frame.pack(side=BOTTOM, fill=X)

    def pack(self, cnf={}, **kw):
        super().pack(cnf, **kw)
        self.pack_children()

    def grid(self, cnf={}, **kw):
        super().grid(cnf, **kw)
        self.pack_children()


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.table_frame = self.__table_frame()
        self.except_table_frame = self.__except_table_frame()


    def __win(self):
        self.title("Tkinter")
        self.geometry("700x600")
        self.minsize(700, 600)
        # self.resizable(width=False, height=False)

    def __table_frame(self):
        table_frame = TableFrame(self)
        table_frame.pack(side=LEFT, fill=BOTH, expand=1)
        return table_frame

    def __except_table_frame(self):
        except_table_frame = ExceptTableFrame(self)
        except_table_frame.pack(side=RIGHT, fill=Y)
        return except_table_frame


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
