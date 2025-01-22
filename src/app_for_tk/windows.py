import tkinter as tk
from tkinter import filedialog as fd
# from tkinter import ttk
# import threading
import pandas as pd
import os
# from time import sleep
# from fileinput import filename


FONT_MAIN_WINDOW = ("Times New Roman", 18)
HEADER_ROW = 1  # номер строки заголовков для парсинга колонок
INDEX = 'Наименование детали'  # столбец индекса
SHEET_VALUES = ['Годных шт.', 'Стоимость вул-ции']  # столбцы для агрегирования
AGG_FUNC = 'sum'  # агрегирующая функция
SUMMARY_SHEET_NAME = 'Сводная'  # название листа сводной таблицы
REFERENCE_SHEET_NAME = 'Справка'  # название листа справки


# Виджет выбора листа для парсинга
class SelectSheetWindow(tk.Toplevel):
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
        self.select_btn = tk.Button(
            self, text="Выбрать", command=self.destroy)

        label.pack(padx=10, pady=10)
        for radio in radios:
            radio.pack(padx=10, anchor=tk.W)
        self.select_btn.pack(side=tk.BOTTOM, pady=10)
        self.focus()

    def select_sheet(self):
        self.grab_set()
        self.wait_window()
        return self.sheet.get()


# Виджет выбора столбцов листа для парсинга
class SelectColumnWindow(tk.Toplevel):
    def __init__(self, width, height, parent, file, sheet):
        super().__init__(parent)
        self.geometry(f"{width}x{height}+200+50")
        self.resizable(False, False)
        self.title("Выбор колонок таблицы")
        label = tk.Label(self, text="Выберите необходимые колонки таблицы")
        self.df = file.parse(sheet, header=HEADER_ROW)
        self.list_cb = []
        for i in range(len(self.df.columns)):
            self.list_cb.append(tk.IntVar(value=1))
        self.checks = [tk.Checkbutton(self, text=self.df.columns[col], variable=self.list_cb[col])
                       for col in range(len(self.df.columns))]
        select_btn = tk.Button(
            self, text="Выбрать", command=self.destroy)
        label.pack(padx=10, pady=10)
        for cb in self.checks:
            cb.pack(padx=10, anchor=tk.W)
        select_btn.pack(side=tk.BOTTOM, pady=10)
        self.focus()

    def select_col(self):
        self.grab_set()
        self.wait_window()
        col = []
        for cb in range(len(self.checks)):
            if self.list_cb[cb].get() == 1:
                col.append(cb)
        return col  # возвращаем столбцы, которые нужны для парсинга


# Виджет главного окна
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
        start_conv = tk.Button(self, text="Создание сводной таблицы и справки",
                               command=self.start_conversion)
        close_btn = tk.Button(self, text="Выход",
                              command=self.destroy)
        self.place_entry = tk.StringVar(value="Text")
        self.place_entry.set("Путь до папки")
        self.entry = tk.Entry(self, width=30,
                              textvariable=self.place_entry)
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=20, sticky="NSEW")
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        folder_select_btn.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        start_conv.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        close_btn.grid(row=3, column=1, padx=10, pady=10, sticky="e")

# Функция выбора папки с файлами(в будущем попробовать askopenfilenames!!)
    def select_folder(self):
        folder = fd.askdirectory()
        self.place_entry.set(folder)
        return folder

# Функция сохранения файла
    def save_file(self, summary, summary_sheet_name, reference, reference_sheet_name):
        file_path = fd.asksaveasfilename(defaultextension='.xlsx')
        if file_path != "":
            with pd.ExcelWriter(file_path, date_format="DD.MM.YY", datetime_format="DD.MM.YY", engine="xlsxwriter") as writer:
                summary.to_excel(
                    writer, sheet_name=summary_sheet_name, index=False)
                reference.to_excel(writer, sheet_name=reference_sheet_name)

    def start_conversion(self):
        # Получение названия папки с файлами Excel(проверить, есть ли файлы, одинаковые ли они...)
        current_folder = self.place_entry.get()
        # Получение пути до папки
        real_folder = os.chdir(current_folder)
        file = os.path.abspath(os.listdir(real_folder)[0])
        # Выбор листа и нужных колонок
        excel_file = pd.ExcelFile(file)
        sheets = excel_file.sheet_names
        radio_win = SelectSheetWindow(300, 400, self, sheets)
        sheet = radio_win.select_sheet()
        columns = SelectColumnWindow(500, 650, self, excel_file, sheet)
        user_cols = columns.select_col()

        # Определение параметров сводной таблицы
        # объединение по выбранному листу из нескольких книг
        df_total = self.summary_sheet(
            current_folder, sheet, user_cols, HEADER_ROW)
        # суммирование значений по наименованию
        reference_list = self.reference_sheet(
            df_total, INDEX, SHEET_VALUES, AGG_FUNC)

        # print(reference_list)
        self.save_file(df_total, SUMMARY_SHEET_NAME,
                       reference_list, REFERENCE_SHEET_NAME)
        self.destroy()

# Функция создания сводной таблицы из нескольких файлов Excel
# с одинаковой шапкой
    def summary_sheet(self, folder_path, nessesary_sheet, use_cols, header_row):
        concat_list = []
        files = os.listdir(folder_path)
        for file in files:
            excel_file = pd.ExcelFile(file)
            sheets = excel_file.sheet_names
            for _ in sheets:
                df = excel_file.parse(
                    sheet_name=nessesary_sheet,
                    header=header_row,
                    usecols=use_cols
                )
            concat_list.append(df)
        # конкатенация датафрейма
        df_total = pd.concat(concat_list, ignore_index=True)
        # удаление пустых строк по столбцу "Прессовщик"
        df_total = df_total[df_total['Прессовщик'] != 0]
        # Сортировка по столбцам 'Дата', 'Прессовщик'
        df_total = df_total.sort_values(by=['Дата', 'Прессовщик'])
        # сброс индексов
        # df_total.reset_index(drop=True, inplace=True)
        return df_total

# функция суммирования значений
    def reference_sheet(self, df, index, values, aggfunc):
        pt = pd.pivot_table(df,
                            values=values,
                            index=index,
                            aggfunc=aggfunc,
                            )
        pt = pt[pt['Годных шт.'] != 0]
        return pt

    def run(self):
        self.mainloop()
