import time
import win32con
from ui import Win
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image
import shutil
import uiautomation as auto
import win32clipboard
import keyboard


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self):
        pass

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui

        self.root_path = os.path.dirname(os.path.abspath(__file__))

        self.CONVERT_OUTPUT_FOLDER_PATH = StringVar()
        self.CONVERT_OUTPUT_FOLDER_PATH.set(os.path.join(self.root_path, "output"))

        self.MAX_LENGTH = IntVar()
        self.MAX_LENGTH.set(1024)
        self.ui.except_table_frame.main_function_frame.image_config_frame.max_image_length_config_scale.set(1024)

        self.ENLARGE_STATE = BooleanVar()
        self.ENLARGE_STATE.set(True)

        self.ui.except_table_frame.main_function_frame.image_config_frame.inquire_enlarge_pic_config_checkbutton.config(variable=self.ENLARGE_STATE)

        self.pics_types_list = ['.bmp', '.jpg', '.jpeg', '.png', '.gif', '.webp']

        self.pics_path_list = []


    def multi_delete_image(self, evt):
        """
        多选删除
        """
        # 反向遍历删除,因为从前往后删除的时候会改变选中项的实际的ID，与之前的ID不一致，导致删除失败出错
        selected_items = reversed(self.ui.table_frame.tree.selection())  # 获取所有选中的项的ID
        for i in selected_items:
            self.ui.table_frame.tree.delete(i)

    def show_image(self, evt):
        item = self.ui.table_frame.tree.focus()
        # 如果没有选中任何（item），则返回
        if not item:
            return
        # 如果选中的item不是图片（是文件夹），则返回
        if self.ui.table_frame.tree.set(item, 'name'):
            return
        pic_folder_node = self.ui.table_frame.tree.parent(item)
        pic_folder_name = self.ui.table_frame.tree.set(pic_folder_node, 'name')
        pic_folder_path = os.path.join(self.ui.table_frame.tree.set(pic_folder_node, 'path'), pic_folder_name)

        pic_name = self.ui.table_frame.tree.set(item, 'path')
        pic_path = os.path.join(pic_folder_path, pic_name).replace('\\', '/')
        pic = Image.open(pic_path)
        pic.show()
        pic.close()

    def get_pics_path_list(self):
        """
        获取所有图片的路径列表
        """
        pics_path_list = []
        for root_item in self.ui.table_frame.tree.get_children():
            pic_folder_name = self.ui.table_frame.tree.set(root_item, 'name')
            pic_folder_path = os.path.join(self.ui.table_frame.tree.set(root_item, 'path'), pic_folder_name)

            for item in self.ui.table_frame.tree.get_children(root_item):
                pic_name = self.ui.table_frame.tree.set(item, 'path')
                pic_path = os.path.join(pic_folder_path, pic_name).replace('\\', '/')
                pics_path_list.append(pic_path)
        return pics_path_list

    @staticmethod
    def resize_gif(input_path, output_path, scale):
        # 打开 GIF 文件
        with Image.open(input_path) as img:
            # 创建一个空列表，用于保存处理后的帧
            frames = []

            try:
                while True:
                    # 对当前帧进行放大
                    new_frame = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
                    frames.append(new_frame)
                    # 移动到下一帧
                    img.seek(img.tell() + 1)
            except EOFError:
                pass  # 到达 GIF 末尾

            # 保存为新的动态 GIF
            frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)

    def convert_image(self, pic_path):
        """
        转换图片
        """
        image_type = os.path.splitext(pic_path)[1].lower()
        hash_part_name=hash(pic_path)

        converted_image_name = f'{hash_part_name}.gif'

        config_max_length = self.MAX_LENGTH.get()
        enlarge_state = self.ENLARGE_STATE.get()
        scale = 1

        # 图片的最长边
        with Image.open(pic_path) as img:
            # 图片的宽度和高度
            width, height = img.size
            # 图片的长边
            max_lenth = max(width, height)

        if max_lenth > config_max_length or enlarge_state:
            # 计算缩放比例
            scale = config_max_length / max_lenth
            # 计算缩放后的宽度和高度
            width = int(width * scale)
            height = int(height * scale)

        converted_image_path = os.path.join(self.CONVERT_OUTPUT_FOLDER_PATH.get(), converted_image_name)
        # 缩放图片
        if image_type == '.gif':
            # 如下图片转换不能简单放大，图片很可能大于微信运行发送的图片的最大值。
            # 经测试，3.67MB的动图也能够发送并能添加为表情包，但是发送时间过长，在没有做出确认图片是否发送成功的功能的时候，
            # 暂时不能加入变大动图的功能
            # if scale != 1:
            #     self.resize_gif(pic_path, converted_image_path, scale)

            # 可以采取先放大后缩小的办法，缺点是损失图片质量
            # 如果放大或者缩小了则转换输出到output，否则直接复制
            if scale != 1:
                self.resize_gif(pic_path, converted_image_path, scale)
            else:
                shutil.copy2(pic_path, converted_image_path)
            # 跳过gif格式的图片
            # shutil.copy2(pic_path, converted_image_path)

            #一直缩小图片，直到图片大小小于等于1.5MB
            # 不直接用下滑线在中间是为了转换后删除最初复制的那张图片,见第177行代码
            converted_image_name = '{}{}.gif'

            a = 1
            while True:

                img_file_size = os.path.getsize(converted_image_path) / 1024 / 1024
                if img_file_size > 1.5:
                    new_converted_image_path = os.path.join(self.CONVERT_OUTPUT_FOLDER_PATH.get(),
                                                            converted_image_name.format(hash_part_name, f'_{a}'))

                    self.resize_gif(converted_image_path, new_converted_image_path, scale=0.7)
                    converted_image_path = new_converted_image_path
                    a += 1

                else:
                    os.remove(os.path.join(self.CONVERT_OUTPUT_FOLDER_PATH.get(),
                                           converted_image_name.format(hash_part_name, '')))
                    for i in range(1, a - 1):
                        os.remove(os.path.join(self.CONVERT_OUTPUT_FOLDER_PATH.get(),
                                               converted_image_name.format(hash_part_name, f'_{i}')))
                    break

        else:
            with Image.open(pic_path) as img:
                # 转换为GIF格式
                img.resize((width, height), Image.LANCZOS).convert('RGBA').save(converted_image_path, 'GIF')

    def start_add_image(self, evt):

        self.ui.except_table_frame.main_function_frame.buttons_frame.start_button.config(state=DISABLED)
        self.ui.except_table_frame.main_function_frame.buttons_frame.select_image_folder_button.config(state=DISABLED)
        self.ui.except_table_frame.main_function_frame.image_config_frame.max_image_length_config_scale.config(state=DISABLED)
        self.ui.except_table_frame.main_function_frame.image_config_frame.inquire_enlarge_pic_config_checkbutton.config(state=DISABLED)
        self.ui.table_frame.tree.config(selectmode="none")

        self.pics_path_list = self.get_pics_path_list()
        self.ui.table_frame.tree.delete(*self.ui.table_frame.tree.get_children())
        for pic_path in self.pics_path_list:
            self.convert_image(pic_path)
        pics_convert_list = [os.path.join(self.CONVERT_OUTPUT_FOLDER_PATH.get(), item) for item in
                             os.listdir(self.CONVERT_OUTPUT_FOLDER_PATH.get())]
        for pic_path in pics_convert_list:
            print(pic_path)
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(pic_path, win32con.CF_UNICODETEXT)
            text = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            notepadWindow = auto.WindowControl(Depth=1, ClassName='ChatWnd', Name='文件传输助手')
            if not auto.WaitForExist(notepadWindow, 8):
                print('文件传输助手窗口未找到，请打开文件传输助手窗口')
                break
            notepadWindow.SetActive()
            notepadWindow.SetTopmost(True)
            time.sleep(1)
            sendFilesButton = notepadWindow.ButtonControl(depth=11, Name='发送文件')
            sendFilesButton.Click(simulateMove=True)
            time.sleep(1)
            getFilesDialogWindow = notepadWindow.WindowControl(Depth=1, Name='打开')
            time.sleep(1)
            # 打开文件对话框时，输入位置直接定位到下方的输入栏了
            keyboard.press_and_release('ctrl+v')
            time.sleep(1)
            keyboard.press_and_release('enter')
            time.sleep(1)
            keyboard.press_and_release('enter')
            time.sleep(1)
            informationListControl = notepadWindow.ListControl(Depth=9, Name='消息')
            time.sleep(1)
            image = informationListControl.GetLastChildControl()
            image.Click()
            # 等待图片发送成功
            time.sleep(10)
            # Application键是Windows系统的特殊键，为书页键，效果为右键菜单
            keyboard.send('Application')
            time.sleep(1)
            MenuItemControl = notepadWindow.MenuItemControl(Name='添加到表情', depth=4)
            time.sleep(1)

            if not auto.WaitForExist(MenuItemControl, 3):
                keyboard.press_and_release('Esc')
                continue
            MenuItemControl.Click(simulateMove=True)
            time.sleep(1)

        self.ui.except_table_frame.main_function_frame.buttons_frame.start_button.config(state=NORMAL)
        self.ui.except_table_frame.main_function_frame.buttons_frame.select_image_folder_button.config(state=NORMAL)
        self.ui.except_table_frame.main_function_frame.image_config_frame.max_image_length_config_scale.config(state=NORMAL)
        self.ui.except_table_frame.main_function_frame.image_config_frame.inquire_enlarge_pic_config_checkbutton.config(state=NORMAL)
        self.ui.table_frame.tree.config(selectmode='extended')
        # 删除output文件夹下的所有文件
        for item in os.listdir(self.CONVERT_OUTPUT_FOLDER_PATH.get()):
            os.remove(os.path.join(self.CONVERT_OUTPUT_FOLDER_PATH.get(), item))

    def select_image_folder(self, evt):
        dir_ = filedialog.askdirectory()
        # 如果没有选择文件夹，则返回
        if not dir_:
            return
        dir_name = os.path.basename(dir_)

        # 如果选择的文件夹已经存在列表中，则不再添加
        if dir_name in [self.ui.table_frame.tree.set(item, 'name') for item in self.ui.table_frame.tree.get_children()]:
            return
        dir_path = os.path.dirname(dir_)
        father = self.ui.table_frame.tree.insert('', END, open=False, text='', values=(dir_name, dir_path,))
        pics_name_list = [item for item in os.listdir(dir_) if
                          os.path.splitext(item)[1].lower() in self.pics_types_list]
        # 如果文件夹下没有图片，则返回
        if not pics_name_list:
            return
        for pic_name in pics_name_list:
            self.ui.table_frame.tree.insert(father, END, open=True, text='', values=('', pic_name))

    def set_max_length(self, evt):
        self.MAX_LENGTH.set(self.ui.except_table_frame.main_function_frame.image_config_frame.max_image_length_config_scale.get())
        print("设置最大长度为:", self.MAX_LENGTH.get())
