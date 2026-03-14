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
        logger.info("程序启动 - xwguidecompress 0.6.0.202603141446")
        logger.debug(f"操作系统: {os.name}")
        logger.debug(f"工作目录: {os.getcwd()}")

        self.root = root
        self.root.title("xwguidecompress 0.6.0.202603141446")
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

        extract_output_frame = ttk.Frame(parent)
        extract_output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        extract_output_label = ttk.Label(extract_output_frame, text="输出路径:")
        extract_output_label.pack(side=tk.LEFT, padx=(0, 5))

        self.extract_output_var = tk.StringVar()
        extract_output_entry = ttk.Entry(extract_output_frame, textvariable=self.extract_output_var, width=40)
        extract_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        extract_output_select_btn = ttk.Button(extract_output_frame, text="选择", command=self.on_extract_output_select)
        extract_output_select_btn.pack(side=tk.LEFT)

        extract_start_btn = ttk.Button(parent, text="开始解压", command=self.on_extract_start)
        extract_start_btn.grid(row=3, column=0, sticky=tk.W, pady=(5, 20))

    def create_compress_section(self, parent):
        """创建压缩功能区域。

        Args:
            parent: 父级容器框架。
        """
        compress_label = ttk.Label(parent, text="压缩", font=("Arial", 12, "bold"))
        compress_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 10))

        compress_path_frame = ttk.Frame(parent)
        compress_path_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        compress_path_label = ttk.Label(compress_path_frame, text="文件路径:")
        compress_path_label.pack(side=tk.LEFT, padx=(0, 5))

        self.compress_path_var = tk.StringVar()
        compress_path_entry = ttk.Entry(compress_path_frame, textvariable=self.compress_path_var, width=40)
        compress_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.compress_type_var = tk.StringVar(value="文件")
        compress_type_combobox = ttk.Combobox(compress_path_frame, textvariable=self.compress_type_var, values=["文件", "文件夹"], width=8, state="readonly")
        compress_type_combobox.pack(side=tk.LEFT, padx=(0, 5))
        compress_type_combobox.bind("<<ComboboxSelected>>", self.on_compress_type_changed)

        compress_select_btn = ttk.Button(compress_path_frame, text="选择", command=self.on_compress_select)
        compress_select_btn.pack(side=tk.LEFT)

        compress_output_frame = ttk.Frame(parent)
        compress_output_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        compress_output_label = ttk.Label(compress_output_frame, text="输出路径:")
        compress_output_label.pack(side=tk.LEFT, padx=(0, 5))

        self.compress_output_var = tk.StringVar()
        compress_output_entry = ttk.Entry(compress_output_frame, textvariable=self.compress_output_var, width=40)
        compress_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        compress_output_select_btn = ttk.Button(compress_output_frame, text="选择", command=self.on_compress_output_select)
        compress_output_select_btn.pack(side=tk.LEFT)

        compress_start_btn = ttk.Button(parent, text="开始压缩", command=self.on_compress_start)
        compress_start_btn.grid(row=7, column=0, sticky=tk.W, pady=(5, 0))

    def on_extract_select(self):
        """处理解压文件选择按钮点击事件。"""
        logger.debug("用户点击'选择'按钮（解压）")
        source_path = filedialog.askopenfilename(title="选择要解压的文件")
        if source_path:
            self.extract_path_var.set(source_path)
            try:
                file_size = os.path.getsize(source_path)
                file_size_mb = file_size / (1024 * 1024)
                logger.info(f"用户选择解压文件: {source_path}")
                logger.debug(f"文件大小: {file_size} 字节 ({file_size_mb:.2f} MB)")
            except OSError as e:
                logger.warning(f"无法获取文件大小: {source_path}, 错误: {e}")
                logger.info(f"用户选择解压文件: {source_path}")
        else:
            logger.debug("用户取消文件选择（解压）")

    def on_extract_output_select(self):
        """处理解压输出路径选择按钮点击事件。"""
        logger.debug("用户点击'选择'按钮（解压输出路径）")
        output_dir = filedialog.askdirectory(title="选择解压输出目录")
        if output_dir:
            self.extract_output_var.set(output_dir)
            logger.info(f"用户选择解压输出目录: {output_dir}")
        else:
            logger.debug("用户取消输出目录选择（解压）")

    def on_extract_start(self):
        """处理开始解压按钮点击事件，将 zip 文件解压到同名目录。"""
        logger.debug("用户点击'开始解压'按钮")
        source_path = self.extract_path_var.get()
        if not source_path:
            messagebox.showwarning("提示", "请选择要解压的文件")
            logger.warning("用户未选择文件即点击解压")
            return

        if not source_path.lower().endswith('.zip'):
            messagebox.showwarning("提示", "仅支持 .zip 格式的文件")
            logger.warning(f"文件格式不支持: {source_path}")
            return

        if not os.path.exists(source_path):
            messagebox.showwarning("提示", "所选文件不存在")
            logger.error(f"源路径不存在: {source_path}")
            return

        source_dir = os.path.dirname(source_path)
        source_name = os.path.splitext(os.path.basename(source_path))[0]

        output_path = self.extract_output_var.get()
        if output_path:
            extract_dir = output_path
        else:
            extract_dir = os.path.join(source_dir, source_name)

        logger.info(f"准备解压: {source_path}")
        logger.debug(f"目标解压目录: {extract_dir}")

        try:
            os.makedirs(extract_dir, exist_ok=True)
            logger.debug(f"创建解压目录: {extract_dir}")

            extracted_files = []
            total_extracted_size = 0

            with zipfile.ZipFile(source_path, 'r') as zip_ref:
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
        except OSError as e:
            error_trace = traceback.format_exc()
            logger.error(f"解压失败 - 系统错误: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "系统错误，无法完成解压")
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"解压失败 - 未知错误: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "解压失败，请查看控制台或日志了解详情")

    def on_compress_type_changed(self, event=None):
        """处理压缩类型选择变化事件。"""
        selected_type = self.compress_type_var.get()
        logger.debug(f"用户切换压缩类型为: {selected_type}")

    def on_compress_select(self):
        """处理压缩文件选择按钮点击事件，根据下拉选择栏的值选择文件或文件夹。"""
        logger.debug("用户点击'选择'按钮（压缩）")

        select_type = self.compress_type_var.get()
        if select_type == "文件":
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
        else:
            folder_path = filedialog.askdirectory(title="选择要压缩的文件夹")
            if folder_path:
                self.compress_path_var.set(folder_path)
                try:
                    total_size = 0
                    file_count = 0
                    for root_dir, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            try:
                                total_size += os.path.getsize(file_path)
                                file_count += 1
                            except OSError:
                                pass
                    total_size_mb = total_size / (1024 * 1024)
                    logger.info(f"用户选择压缩文件夹: {folder_path}")
                    logger.debug(f"文件夹包含 {file_count} 个文件，总大小: {total_size} 字节 ({total_size_mb:.2f} MB)")
                except Exception as e:
                    logger.warning(f"无法获取文件夹信息: {folder_path}, 错误: {e}")
                    logger.info(f"用户选择压缩文件夹: {folder_path}")
            else:
                logger.debug("用户取消文件夹选择（压缩）")

    def on_compress_output_select(self):
        """处理压缩输出路径选择按钮点击事件。"""
        logger.debug("用户点击'选择'按钮（压缩输出路径）")
        output_dir = filedialog.askdirectory(title="选择压缩输出目录")
        if output_dir:
            self.compress_output_var.set(output_dir)
            logger.info(f"用户选择压缩输出目录: {output_dir}")
        else:
            logger.debug("用户取消输出目录选择（压缩）")

    def on_compress_start(self):
        """处理开始压缩按钮点击事件，将文件或文件夹压缩为 zip 格式。"""
        logger.debug("用户点击'开始压缩'按钮")
        source_path = self.compress_path_var.get()
        if not source_path:
            messagebox.showwarning("提示", "请选择要压缩的文件或文件夹")
            logger.warning("用户未选择内容即点击压缩")
            return

        if not os.path.exists(source_path):
            messagebox.showwarning("提示", "所选文件或文件夹不存在")
            logger.error(f"路径不存在: {source_path}")
            return

        source_dir = os.path.dirname(source_path)
        source_name = os.path.basename(source_path)

        if os.path.isdir(source_path):
            zip_filename = f"{source_name}.zip"
        else:
            name_without_ext = os.path.splitext(source_name)[0]
            zip_filename = f"{name_without_ext}_压缩.zip"

        output_dir = self.compress_output_var.get()
        if output_dir:
            zip_path = os.path.join(output_dir, zip_filename)
        else:
            zip_path = os.path.join(source_dir, zip_filename)

        counter = 1
        original_zip_path = zip_path
        while os.path.exists(zip_path):
            name, ext = os.path.splitext(original_zip_path)
            zip_path = f"{name}_{counter}{ext}"
            counter += 1

        logger.info(f"准备压缩: {source_path}")
        logger.debug(f"输出 zip 文件: {zip_path}")

        try:
            total_files = 0
            total_original_size = 0

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isdir(source_path):
                    logger.debug(f"开始压缩文件夹: {source_path}")
                    for root_dir, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            arcname = os.path.relpath(file_path, source_path)
                            try:
                                file_size = os.path.getsize(file_path)
                                total_original_size += file_size
                                zipf.write(file_path, arcname)
                                total_files += 1
                                logger.debug(f"已添加: {arcname} ({file_size} 字节)")
                            except OSError as e:
                                logger.warning(f"无法读取文件，已跳过: {file_path}, 错误: {e}")
                else:
                    logger.debug(f"开始压缩文件: {source_path}")
                    file_size = os.path.getsize(source_path)
                    total_original_size = file_size
                    arcname = source_name
                    zipf.write(source_path, arcname)
                    total_files = 1
                    logger.debug(f"已添加: {arcname} ({file_size} 字节)")

            compressed_size = os.path.getsize(zip_path)
            compressed_size_mb = compressed_size / (1024 * 1024)
            original_size_mb = total_original_size / (1024 * 1024)

            if total_original_size > 0:
                compression_ratio = (1 - compressed_size / total_original_size) * 100
            else:
                compression_ratio = 0

            logger.info(f"压缩成功 - 共压缩 {total_files} 个文件")
            logger.debug(f"原始大小: {total_original_size} 字节 ({original_size_mb:.2f} MB)")
            logger.debug(f"压缩后大小: {compressed_size} 字节 ({compressed_size_mb:.2f} MB)")
            logger.debug(f"压缩率: {compression_ratio:.1f}%")
            logger.debug(f"输出文件: {zip_path}")

            messagebox.showinfo("成功", "压缩成功")

        except PermissionError as e:
            error_trace = traceback.format_exc()
            logger.error(f"压缩失败 - 权限不足: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "权限不足，无法创建或写入压缩文件")
        except OSError as e:
            error_trace = traceback.format_exc()
            logger.error(f"压缩失败 - 系统错误: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "系统错误，无法完成压缩")
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"压缩失败 - 未知错误: {e}")
            logger.debug(f"异常堆栈:\n{error_trace}")
            messagebox.showerror("错误", "压缩失败，请查看控制台或日志了解详情")
