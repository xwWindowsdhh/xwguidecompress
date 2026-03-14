import logging
import os
import traceback
import zipfile
from datetime import datetime

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_filename = f"app_{datetime.now().strftime('%Y%m%d')}.log"
log_path = os.path.join(log_dir, log_filename)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class XWGuideCompressApp:
    """XWGuide 压缩工具的主应用类，提供文件解压和压缩功能。"""

    def __init__(self, root):
        """初始化应用窗口和界面组件。

        Args:
            root: Tkinter 根窗口实例。
        """
        logger.info("=" * 50)
        logger.info("程序启动 - xwguidecompress 0.1.0.202603141058-alpha.2")
        logger.debug(f"操作系统: {os.name}")
        logger.debug(f"工作目录: {os.getcwd()}")

        self.root = root
        self.root.title("xwguidecompress 0.1.0.202603141058-alpha.2")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.create_widgets()
        logger.info("界面初始化完成")

        self.root.update_idletasks()
        self.root.geometry('')
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
        logger.debug("用户点击'选择'按钮（解压）")
        file_path = filedialog.askopenfilename(title="选择要解压的文件")
        if file_path:
            self.extract_path_var.set(file_path)
            try:
                file_size = os.path.getsize(file_path)
                file_size_mb = file_size / (1024 * 1024)
                logger.info(f"用户选择解压文件: {file_path}")
                logger.debug(f"文件大小: {file_size} 字节 ({file_size_mb:.2f} MB)")
            except OSError as e:
                logger.warning(f"无法获取文件大小: {file_path}, 错误: {e}")
                logger.info(f"用户选择解压文件: {file_path}")
        else:
            logger.debug("用户取消文件选择（解压）")

    def on_extract_start(self):
        """处理开始解压按钮点击事件。"""
        logger.debug("用户点击'开始解压'按钮")
        file_path = self.extract_path_var.get()
        if not file_path:
            messagebox.showwarning("提示", "请选择要解压的文件")
            logger.warning("用户未选择文件即点击解压")
            return

        if not file_path.lower().endswith('.zip'):
            messagebox.showwarning("提示", "仅支持 .zip 格式的文件")
            logger.warning(f"文件格式不支持: {file_path}")
            return

        if not os.path.exists(file_path):
            messagebox.showwarning("提示", "所选文件不存在")
            logger.error(f"文件不存在: {file_path}")
            return

        zip_dir = os.path.dirname(file_path)
        zip_name = os.path.splitext(os.path.basename(file_path))[0]
        extract_dir = os.path.join(zip_dir, zip_name)

        try:
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            logger.info(f"准备解压文件: {file_path}")
            logger.debug(f"源文件大小: {file_size} 字节 ({file_size_mb:.2f} MB)")
            logger.debug(f"目标解压目录: {extract_dir}")
        except OSError as e:
            logger.error(f"无法获取源文件信息: {e}")
            logger.info(f"准备解压文件: {file_path}")

        try:
            os.makedirs(extract_dir, exist_ok=True)
            logger.debug(f"创建解压目录: {extract_dir}")

            extracted_files = []
            total_extracted_size = 0

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                logger.debug(f"压缩包内包含 {len(file_list)} 个条目")

                for item in file_list:
                    logger.debug(f"正在解压: {item}")
                    zip_ref.extract(item, extract_dir)
                    extracted_path = os.path.join(extract_dir, item)
                    if os.path.isfile(extracted_path):
                        item_size = os.path.getsize(extracted_path)
                        total_extracted_size += item_size
                        extracted_files.append((item, item_size))
                        logger.debug(f"解压完成: {item} ({item_size} 字节)")

            total_size_mb = total_extracted_size / (1024 * 1024)
            logger.info(f"解压成功 - 共解压 {len(extracted_files)} 个文件")
            logger.debug(f"解压总大小: {total_extracted_size} 字节 ({total_size_mb:.2f} MB)")
            logger.debug(f"输出目录: {extract_dir}")
            messagebox.showinfo("成功", "解压成功")
        except zipfile.BadZipFile as e:
            error_trace = traceback.format_exc()
            logger.error(f"解压失败 - 文件损坏: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "文件损坏或不是有效的压缩文件")
        except RuntimeError as e:
            error_trace = traceback.format_exc()
            logger.error(f"解压失败 - RuntimeError: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            if 'password' in str(e).lower():
                messagebox.showerror("错误", "文件受密码保护，无法解压")
            else:
                messagebox.showerror("错误", "解压失败，请查看控制台或日志了解详情")
        except PermissionError as e:
            error_trace = traceback.format_exc()
            logger.error(f"解压失败 - 权限不足: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "权限不足，无法写入目标目录")
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"解压失败 - 未知错误: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "解压失败，请查看控制台或日志了解详情")

    def on_compress_select(self):
        """处理压缩文件选择按钮点击事件。"""
        logger.debug("用户点击'选择'按钮（压缩）")
        file_path = filedialog.askopenfilename(title="选择要压缩的文件")
        if file_path:
            self.compress_path_var.set(file_path)
            try:
                file_size = os.path.getsize(file_path)
                file_size_mb = file_size / (1024 * 1024)
                logger.info(f"用户选择压缩文件: {file_path}")
                logger.debug(f"文件大小: {file_size} 字节 ({file_size_mb:.2f} MB)")
            except OSError as e:
                logger.warning(f"无法获取文件大小: {file_path}, 错误: {e}")
                logger.info(f"用户选择压缩文件: {file_path}")
        else:
            logger.debug("用户取消文件选择（压缩）")

    def on_compress_start(self):
        """处理开始压缩按钮点击事件。"""
        logger.debug("用户点击'开始压缩'按钮")
        file_path = self.compress_path_var.get()
        if not file_path:
            messagebox.showwarning("提示", "请选择要压缩的文件")
            logger.warning("用户未选择文件即点击压缩")
            return

        logger.info(f"用户尝试压缩文件（功能开发中）: {file_path}")
        messagebox.showinfo("提示", "压缩功能开发中")
