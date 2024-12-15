from tkinter import *
from tkinter import filedialog as fd


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
        button = Button(self.root, text="Button",
                        command=self.select_folder)
        button.configure(text="Выберите папку", command=self.select_folder)
        self.place_entry = StringVar(value="Text")
        self.place_entry.set("Путь до папки")
        self.entry = Entry(self.root, width=30, textvariable=self.place_entry)
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=20, sticky="NSEW")
        self.entry.grid(row=1, column=0, padx=20, pady=20)
        button.grid(row=1, column=1, padx=20, pady=20)

    def select_folder(self):
        folder = fd.askdirectory()
        self.place_entry.set(folder)
        return folder

    def run(self):
        self.root.mainloop()
