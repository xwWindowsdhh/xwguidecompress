import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class XWGuideCompressApp:
    """XWGuide 压缩工具的主应用类，提供文件解压和压缩功能。"""

    def __init__(self, root):
        """初始化应用窗口和界面组件。

        Args:
            root: Tkinter 根窗口实例。
        """
        self.root = root
        self.root.title("xwguidecompress 0.1.0.202603131942-alpha")

        self.create_widgets()

        self.root.update_idletasks()  # 更新界面以计算实际需要的大小
        self.root.geometry('')  # 重置为自动大小
        # 允许用户调整窗口大小
        self.root.resizable(True, True)

        self.root.minsize(400, 250)

    def create_widgets(self):
        """创建主界面框架和各个功能区域。"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_extract_section(main_frame)
        self.create_compress_section(main_frame)

    def create_extract_section(self, parent):
        """创建解压功能区域。

        Args:
            parent: 父级容器框架。
        """
        extract_label = ttk.Label(parent, text="解压", font=("Arial", 12, "bold"))
        extract_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        extract_path_frame = ttk.Frame(parent)
        extract_path_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        extract_path_label = ttk.Label(extract_path_frame, text="文件路径:")
        extract_path_label.pack(side=tk.LEFT, padx=(0, 5))

        self.extract_path_var = tk.StringVar()
        extract_path_entry = ttk.Entry(extract_path_frame, textvariable=self.extract_path_var, width=40)
        extract_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        extract_select_btn = ttk.Button(extract_path_frame, text="选择", command=self.on_extract_select)
        extract_select_btn.pack(side=tk.LEFT)

        extract_start_btn = ttk.Button(parent, text="开始解压", command=self.on_extract_start)
        extract_start_btn.grid(row=2, column=0, sticky=tk.W, pady=(5, 20))

    def create_compress_section(self, parent):
        """创建压缩功能区域。

        Args:
            parent: 父级容器框架。
        """
        compress_label = ttk.Label(parent, text="压缩", font=("Arial", 12, "bold"))
        compress_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))

        compress_path_frame = ttk.Frame(parent)
        compress_path_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        compress_path_label = ttk.Label(compress_path_frame, text="文件路径:")
        compress_path_label.pack(side=tk.LEFT, padx=(0, 5))

        self.compress_path_var = tk.StringVar()
        compress_path_entry = ttk.Entry(compress_path_frame, textvariable=self.compress_path_var, width=40)
        compress_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        compress_select_btn = ttk.Button(compress_path_frame, text="选择", command=self.on_compress_select)
        compress_select_btn.pack(side=tk.LEFT)

        compress_start_btn = ttk.Button(parent, text="开始压缩", command=self.on_compress_start)
        compress_start_btn.grid(row=5, column=0, sticky=tk.W, pady=(5, 0))

    def on_extract_select(self):
        """处理解压文件选择按钮点击事件。"""
        file_path = filedialog.askopenfilename(title="选择要解压的文件")
        if file_path:
            self.extract_path_var.set(file_path)

    def on_extract_start(self):
        """处理开始解压按钮点击事件。"""
        file_path = self.extract_path_var.get()
        if not file_path:
            messagebox.showerror("错误", "[解压] 错误: 未选择文件")
            return
        messagebox.showinfo("提示", f"[解压] 开始解压: {file_path}")

    def on_compress_select(self):
        """处理压缩文件选择按钮点击事件。"""
        file_path = filedialog.askopenfilename(title="选择要压缩的文件")
        if file_path:
            self.compress_path_var.set(file_path)

    def on_compress_start(self):
        """处理开始压缩按钮点击事件。"""
        file_path = self.compress_path_var.get()
        if not file_path:
            messagebox.showerror("错误", "[压缩] 错误: 未选择文件")
            return
        messagebox.showinfo("提示", f"[压缩] 开始压缩: {file_path}")