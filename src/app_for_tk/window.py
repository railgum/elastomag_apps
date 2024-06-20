from tkinter import *
from tkinter import filedialog as fd


class Window:
    def __init__(self, width, height, title="MyWindow", resizable=(False, False), icon=None):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+200+200")
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(icon)
        self.label = Label(
            self.root,
            text="Label",
            font=("Times New Roman", 18)
        )
        self.button = Button(self.root, text="Button",
                             command=self.select_folder)
        self.place_entry = StringVar(value="Text")
        self.entry = Entry(self.root, width=30, textvariable=self.place_entry)

    def run(self):
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        self.label.grid(row=0, column=0, columnspan=2,
                        padx=20, pady=20, sticky="NSEW")
        self.entry.grid(row=1, column=0, padx=20, pady=20)
        self.button.grid(row=1, column=1, padx=20, pady=20)

    def select_folder(self):
        folder = fd.askdirectory()
        self.place_entry.set(folder)
        return folder


if __name__ == "__main__":
    window = Window(500, 500)
    window.run()
