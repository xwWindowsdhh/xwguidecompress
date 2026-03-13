import tkinter as tk
from gui import XWGuideCompressApp


def main():
    """应用程序入口函数。"""
    root = tk.Tk()
    app = XWGuideCompressApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
