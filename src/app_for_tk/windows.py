from functions import *
from tkinter import *
from tkinter import filedialog as fd
import pandas as pd

FONT_MAIN_WINDOW = ("Times New Roman", 18)


class Main_Window:
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
        folder_select_but = Button(self.root)
        folder_select_but.configure(
            text="Выберите папку", command=self.select_folder)
        start_creation_but = Button(self.root)
        start_creation_but.configure(
            text="Запуск", command=self.start_creation)

        self.place_entry = StringVar(value="Text")
        self.place_entry.set("Путь до папки")
        self.entry = Entry(self.root, width=30, textvariable=self.place_entry)
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=20, sticky="NSEW")
        self.entry.grid(row=1, column=0, padx=20, pady=20)
        folder_select_but.grid(row=1, column=1, padx=20, pady=20)
        start_creation_but.grid(row=2, column=1, padx=20, pady=20)

    def select_folder(self):
        folder = fd.askdirectory()
        self.place_entry.set(folder)
        return folder

    def start_creation(self):
        current_folder = self.place_entry.get()
        real_folder = os.chdir(current_folder)
        file = os.path.abspath(os.listdir(real_folder)[0])
        print(file)
        if file.endswith('.xlsx'):
            excel_file = pd.ExcelFile(file)
            sheets = excel_file.sheet_names
            print(sheets)
        return real_folder

    def run(self):
        self.root.mainloop()
