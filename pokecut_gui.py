import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import tkinter as tk
from tkinter import filedialog, messagebox
import asyncio
from backend.pokecut import run_backend

def run_from_gui(folder, width, height, fmt, concurrency):
    if not folder:
        messagebox.showerror("Lỗi", "Bạn phải chọn thư mục ảnh!")
        return
    try:
        asyncio.run(run_backend(folder, width, height, fmt, concurrency))
        messagebox.showinfo("Hoàn thành", "Xử lý ảnh thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def main():
    root = tk.Tk()
    root.title("Pokecut GUI")

    # Folder ảnh
    tk.Label(root, text="Folder ảnh:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    folder_var = tk.StringVar()
    tk.Entry(root, textvariable=folder_var, width=40).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Chọn...", command=lambda: folder_var.set(filedialog.askdirectory())).grid(row=0, column=2, padx=5, pady=5)

    # Width
    tk.Label(root, text="Chiều rộng:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    width_var = tk.IntVar(value=1024)
    tk.Entry(root, textvariable=width_var).grid(row=1, column=1, padx=5, pady=5)

    # Height
    tk.Label(root, text="Chiều cao:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    height_var = tk.IntVar(value=1024)
    tk.Entry(root, textvariable=height_var).grid(row=2, column=1, padx=5, pady=5)

    # Format
    tk.Label(root, text="Định dạng:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    fmt_var = tk.StringVar(value="jpg")
    tk.OptionMenu(root, fmt_var, "jpg", "png").grid(row=3, column=1, padx=5, pady=5)

    # Concurrency
    tk.Label(root, text="Số browser:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    cc_var = tk.IntVar(value=1)
    tk.Spinbox(root, from_=1, to=5, textvariable=cc_var).grid(row=4, column=1, padx=5, pady=5)

    # Nút Run
    tk.Button(
        root,
        text="Chạy",
        command=lambda: run_from_gui(
            folder_var.get(),
            width_var.get(),
            height_var.get(),
            fmt_var.get(),
            cc_var.get()
        )
    ).grid(row=5, column=0, columnspan=3, pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()
