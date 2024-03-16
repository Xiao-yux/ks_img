from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import base64
import io
import png
import threading

ocr_recognize = png.ocr_recognize

P = Path("./img")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('测试程序1')
        self.geometry('700x500')

        self.pages = {}
        self.create_widgets()

    def create_widgets(self):
        # 创建左侧的按钮
        frame_buttons = tk.Frame(self)
        frame_buttons.pack(side=tk.LEFT, fill=tk.Y)

        btn_home = tk.Button(frame_buttons, text='首页', command=self.show_page_home)
        btn_home.pack(side=tk.TOP, fill=tk.X)

        btn_identify = tk.Button(frame_buttons, text='识别', command=self.show_page_identify)
        btn_identify.pack(side=tk.TOP, fill=tk.X)

        btn_output = tk.Button(frame_buttons, text='输出', command=self.show_page_output)
        btn_output.pack(side=tk.TOP, fill=tk.X)

        # 创建各个页面
        self.pages['home'] = self.create_page_home()
        self.pages['identify'] = self.create_page_identify()
        self.pages['output'] = self.create_page_output()

    def run_png(self):
        def task():
            for i in P.iterdir():
                result, img_str = ocr_recognize(i)
                if isinstance(result, list):  # 如果结果是列表，将其转换为字符串
                    result = '\n'.join(result)
                self.pages['output'].txt_output.insert(tk.END, result + "\n")
                self.add_image(img_str)
        threading.Thread(target=task).start() #新开一个线程执行函数，防止卡顿


    def create_page_home(self):
        frame_home = tk.Frame(self)
        frame_home.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        button = tk.Button(frame_home, text='运行', command=self.run_png)
        button.pack()
        lbl_title = tk.Label(frame_home, text='Main')
        lbl_title.pack(side=tk.TOP, pady=20)

        return frame_home
    

    def create_page_identify(self):
        frame_identify = tk.Frame(self)

        # 创建一个 Canvas 小部件和一个垂直 Scrollbar 小部件
        frame_identify.canvas = tk.Canvas(frame_identify, bg='white')
        frame_identify.scrollbar = tk.Scrollbar(frame_identify, orient='vertical', command=frame_identify.canvas.yview)

        # 创建一个 Frame 小部件，用于放置图片
        frame_identify.frame_images = tk.Frame(frame_identify.canvas)

        # 将 Scrollbar 配置为 Canvas 的 yscrollcommand
        frame_identify.canvas.configure(yscrollcommand=frame_identify.scrollbar.set)

        # 将 Frame 小部件添加到 Canvas 中
        frame_identify.canvas.create_window((0, 0), window=frame_identify.frame_images, anchor='nw')

        # 当 Frame 小部件的大小改变时，更新 Canvas 的滚动区域
        frame_identify.frame_images.bind('<Configure>', lambda e: frame_identify.canvas.configure(scrollregion=frame_identify.canvas.bbox('all')))

        # 将 Canvas 和 Scrollbar 小部件放置到 IdentifyPage 中
        frame_identify.canvas.pack(side='left', fill='both', expand=True)
        frame_identify.scrollbar.pack(side='right', fill='y')

        return frame_identify
    
    def add_image(self, img_str):
        # 从 base64 字符串中加载图片
        image = Image.open(io.BytesIO(base64.b64decode(img_str)))
        photo = ImageTk.PhotoImage(image)

        # 创建一个 Label 小部件，用于显示图片
        label = tk.Label(self.pages['identify'].frame_images, image=photo)
        label.image = photo  # 需要保持对 PhotoImage 的引用

        # 将 Label 小部件添加到 Frame 中
        label.pack(padx=5, pady=5)

    def create_page_output(self):
        frame_output = tk.Frame(self)
        frame_output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        frame_output.txt_output = tk.Text(frame_output)
        frame_output.txt_output.pack(fill=tk.BOTH, expand=True)

        return frame_output

    def show_page_home(self):
        self.hide_all_pages()
        self.pages['home'].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_page_identify(self):
        self.hide_all_pages()
        self.pages['identify'].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_page_output(self):
        self.hide_all_pages()
        self.pages['output'].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def hide_all_pages(self):
        for page in self.pages.values():
            page.pack_forget()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
