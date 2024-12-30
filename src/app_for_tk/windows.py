from functions import *
import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd

FONT_MAIN_WINDOW = ("Times New Roman", 18)


class SecondWindow(tk.Toplevel):
    def __init__(self, width, height, parent, sheets):
        super().__init__(parent)
        self.geometry(f"{width}x{height}+200+200")
        self.resizable(False, False)
        self.title("Выбор таблицы")
        self.sheets = sheets
        self.sheet = tk.StringVar()
        self.sheet.set(sheets[0])
        label = tk.Label(
            self, text="Выберите лист для создания сводной таблицы")
        radios = [tk.Radiobutton(self, text=t, value=t,
                                 variable=self.sheet) for t in sheets]
        select_btn = tk.Button(self, text="Выбрать", command=self.select_radio)
        close_btn = tk.Button(self, text="Закрыть", command=self.destroy)

        label.pack(padx=10, pady=10)
        for radio in radios:
            radio.pack(padx=10, anchor=tk.W)
        select_btn.pack(side=tk.LEFT, padx=5)
        close_btn.pack(side=tk.RIGHT)
        self.focus()
        self.grab_set()

    def select_radio(self):
        # print(self.sheet.get())
        return self.sheet.get()


class MainWindow(tk.Tk):
    def __init__(self, width, height, title="MyWindow", resizable=(False, False), icon=None):
        super().__init__()
        self.label = None
        self.entry = None
        self.place_entry = None
        self.title(title)
        self.geometry(f"{width}x{height}+200+200")
        self.resizable(resizable[0], resizable[1])
        if icon:
            self.iconbitmap(icon)

        self.draw_widgets()

    def draw_widgets(self):
        self.label = tk.Label(
            self,
            text="Label",
            font=FONT_MAIN_WINDOW
        )
        folder_select_btn = tk.Button(
            self, text="Выберите папку", command=self.select_folder)
        select_sheet_btn = tk.Button(
            self, text="Запуск", command=self.select_sheet)
        close_btn = tk.Button(self, text="Выход",
                              command=self.destroy)
        self.place_entry = tk.StringVar(value="Text")
        self.place_entry.set("Путь до папки")
        self.entry = tk.Entry(self, width=30,
                              textvariable=self.place_entry)
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=20, sticky="NSEW")
        self.entry.grid(row=1, column=0, padx=20, pady=20)
        folder_select_btn.grid(row=1, column=1, padx=20, pady=20)
        select_sheet_btn.grid(row=2, column=0, padx=10, pady=10)
        close_btn.grid(row=2, column=1, padx=10, pady=10)

    def select_folder(self):
        folder = fd.askdirectory()
        self.place_entry.set(folder)
        return folder

    def select_sheet(self):
        current_folder = self.place_entry.get()
        real_folder = os.chdir(current_folder)
        file = os.path.abspath(os.listdir(real_folder)[0])
        sheets = []
        if file.endswith('.xlsx'):
            excel_file = pd.ExcelFile(file)
            sheets = excel_file.sheet_names
            radio_win = SecondWindow(300, 400, self, sheets)
            return radio_win.select_radio()
        # else:
        #     return msgerr
        # print(sheets)

    def run(self):
        self.mainloop()
