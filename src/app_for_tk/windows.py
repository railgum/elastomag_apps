from functions import *
from tkinter import *
from tkinter import filedialog as fd
import pandas as pd

FONT_MAIN_WINDOW = ("Times New Roman", 18)


class SecondWindow(Toplevel):
    def __init__(self, parent, sheets):
        super().__init__(parent)
        self.config(width=500, height=600)
        self.title("Выбор таблицы")
        self.sheets = sheets
        self.sheet = StringVar()
        self.sheet.set(sheets[0])
        label = Label(self, text="Выберите лист для создания сводной таблицы")
        radios = [Radiobutton(self, text=t, value=t,
                              variable=self.sheet) for t in sheets]
        select_btn = Button(self, text="Выбрать", command=self.select_radio)
        close_btn = Button(self, text="Закрыть", command=self.destroy)

        label.pack(padx=10, pady=10)
        for radio in radios:
            radio.pack(padx=10, anchor=W)
        select_btn.pack(side=LEFT)
        close_btn.pack(side=RIGHT)
        self.focus()
        self.grab_set()

    def select_radio(self):
        return self.sheet.get()


class MainWindow:
    def __init__(self, width, height, title="MyWindow", resizable=(False, False), icon=None):
        self.root = Tk()
        self.label = None
        self.entry = None
        self.place_entry = None
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+200+200")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(icon)

        self.draw_widgets()

    def draw_widgets(self):
        self.label = Label(
            self.root,
            text="Label",
            font=FONT_MAIN_WINDOW
        )
        folder_select_btn = Button(
            self.root, text="Выберите папку", command=self.select_folder)
        start_creation_btn = Button(
            self.root, text="Запуск", command=self.start_creation)
        close_btn = Button(self.root, text="Выход", command=self.root.destroy)
        self.place_entry = StringVar(value="Text")
        self.place_entry.set("Путь до папки")
        self.entry = Entry(self.root, width=30, textvariable=self.place_entry)
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=20, sticky="NSEW")
        self.entry.grid(row=1, column=0, padx=20, pady=20)
        folder_select_btn.grid(row=1, column=1, padx=20, pady=20)
        start_creation_btn.grid(row=2, column=0, padx=10, pady=10)
        close_btn.grid(row=2, column=1, padx=10, pady=10)

    def select_folder(self):
        folder = fd.askdirectory()
        self.place_entry.set(folder)
        return folder

    def start_creation(self):
        current_folder = self.place_entry.get()
        real_folder = os.chdir(current_folder)
        file = os.path.abspath(os.listdir(real_folder)[0])
        sheets = []
        if file.endswith('.xlsx'):
            excel_file = pd.ExcelFile(file)
            sheets = excel_file.sheet_names
            radio_win = SecondWindow(self, sheets)

            return radio_win.select_radio()
        # print(sheets)

    def run(self):
        self.root.mainloop()
