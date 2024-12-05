from tkinter import *
from tkinter.ttk import *
from tkinter import Scale
from tkinter.scrolledtext import ScrolledText


class TableFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tree = self.create_table()
        self.xscroll, self.yscroll = self.create_scrollbars(self.tree)

    def create_table(self):
        # columns = {"图片文件夹名称": 120, "路径": 319}
        tk_table = Treeview(self, show="headings", columns=("图片文件夹名称", "路径"))

        tk_table.column("图片文件夹名称", anchor="center", stretch=False)
        tk_table.heading("图片文件夹名称", text="图片文件夹名称", anchor=CENTER)

        tk_table.column("路径", anchor="center", stretch=True)
        tk_table.heading("路径", text="路径", anchor='center')
        # for text, width in columns.items():  # 批量设置列属性
        #     tk_table.heading(text, text=text, anchor='center')
        #     tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        # tree = Treeview(self, columns="path")
        # tree.column("#0", anchor=CENTER)
        # tree.column("path", anchor=CENTER)
        # tree.heading('#0', text='name')
        # tree.heading('path', text='path')
        return tk_table

    def create_scrollbars(self, tree):
        xscroll = Scrollbar(self, orient=HORIZONTAL)
        yscroll = Scrollbar(self, orient=VERTICAL)
        tree.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        xscroll.config(command=tree.xview)
        yscroll.config(command=tree.yview)
        return xscroll, yscroll

    def pack_children(self):
        self.xscroll.pack(side=BOTTOM, fill=X, expand=False)
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
        # self.profile_photo_label = self.create_profile_photo_label()
        self.about_scroll_text = self.create_about_scroll_text()

    def create_profile_photo_label(self):
        photo = PhotoImage(file="profile.gif")
        label = Label(self, image=photo)
        label.image = photo
        return label

    def create_about_scroll_text(self):
        text = """微信自动添加表情包助手  
b站账号：Z在此


（双击说明窗口可以打开独立窗口查看）


程序功能：将指定文件夹内的图片添加到你的微信的表情包库中。

与很多其他添加微信表情包的程序一样，本程序也有一些限制和问题：
    1.程序运行过程中你不能在电脑中进行其他任何操作，因为程序使用了操控键盘输入和鼠标光标的库。

    2.程序虽然可以自动将大图片转化为小图片，但是图片质量越大转换时间越长，因此尽量不要选择质量过大的图片或者自己先手动缩小再添加到选择的文件夹内。

    3.由于本人技术限制，程序存在bug，bug发生时无法继续添加表情包，而程序仍会持续运行。此时要么只能等待程序自行结束，或者乘添加表情包光标停止的时间的间隙自己手动关了程序窗口（。bug并不会导致额外的什么问题（因为定位都在微信上）。



程序使用说明：
    将文件传输助手窗口独立出来，！！尽可能拉长拉大！！，运行时程序会自动将文件传输助手窗口置顶。此时再打开程序配置好选项后就可以开始了。



配置说明:

表格：
    选择的所有的图片文件夹的名称和路径，还有图片名称都显示在里面。双击项展开文件夹项，显示该文件夹下的图片名称，双击图片项以本地默认图片浏览打开预览（动图的浏览是截取的第一帧的静态图）。可以按ctrl+左键多选按delete删除对应不需要的项。


图片配置说明：
    图片边长：设置微信表情包的最大边长（1~1024），图片的最长边超过设定的长度将被自动缩小至等于所设定的长度。


放大边长小于设定值的图片：
    如果选中此选项，程序会将最长边小于设定值的图片放大到设定值；如果不选中，则图片保持原大小添加到表情包库中。


"""
        # text = """123"""

        text_ = ScrolledText(self, wrap=WORD, width=36)
        text_.insert(END, text)
        return text_

    def pack_children(self):
        # self.profile_photo_label.pack(side=TOP, fill=BOTH, padx=8, pady=3)
        self.about_scroll_text.pack(side=TOP, fill=BOTH, expand=1, padx=8, pady=3)

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
        scale = Scale(self, from_=1, to=1024, orient=HORIZONTAL, label="图片边长（1~1024）", width=20)
        return scale

    def create_inquire_enlarge_pic_config_checkbutton(self):
        checkbutton = Checkbutton(self, text="放大边长小于设定值的图片", variable=IntVar(), onvalue=1,
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
        self.size_grip = self.create_size_grip()

    def create_size_grip(self):
        size_grip = Sizegrip(self)
        return size_grip

    def create_image_config_frame(self):
        image_config_frame = ImageConfigLabelFrame(self, text="图片配置")
        return image_config_frame

    def pack_children(self):
        self.buttons_frame.pack(side=TOP, fill=None, padx=8, pady=3, expand=1)
        self.image_config_frame.pack(side=TOP, fill=None, padx=8, pady=3, expand=1)
        self.size_grip.pack(side=BOTTOM, padx=8, pady=3, anchor=E)
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
        # self.geometry("700x600")
        self.minsize(800, 800)
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
        self.ctl.init(self)
        self.except_table_frame.main_function_frame.image_config_frame.inquire_enlarge_pic_config_checkbutton.config(
            variable=self.ctl.ENLARGE_STATE)

    def __event_bind(self):
        self.bind("<Configure>", self.ctl.fix_tree_column_width)

        self.table_frame.tree.bind('<Double-Button-1>', self.ctl.show_image)
        self.table_frame.tree.bind('<Delete>', self.ctl.multi_delete_image)
        self.table_frame.tree.bind("<B1-Motion>", self.ctl.fix_tree_column_width)
        self.table_frame.tree.bind("<ButtonRelease-1>", self.ctl.fix_tree_column_width)

        self.except_table_frame.introduction_frame.about_scroll_text.bind('<Double-Button-1>',self.ctl.show_introduction_toplevel)

        self.except_table_frame.main_function_frame.buttons_frame.start_button.bind('<Button-1>',
                                                                                    self.ctl.start_add_image)
        self.except_table_frame.main_function_frame.buttons_frame.select_emoji_folder_button.bind('<Button-1>',
                                                                                                  self.ctl.select_image_folder)
        self.except_table_frame.main_function_frame.image_config_frame.max_image_length_config_scale.bind('<B1-Motion>',
                                                                                                          self.ctl.set_max_length)

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
