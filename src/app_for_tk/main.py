from window import Window


window = Window(700, 300, "Создание справки и сводной таблицы",
                icon=None)
window.label.configure(
    text="@Автор программы - Раиль Гумеров.\nПриветствую вас в моем первом .exe-шном приложении!",
    fg="green"
)
window.button.configure(text="Выберите папку", command=window.select_folder)
window.place_entry.set("Путь до папки")

window.entry.configure(width=50, fg="blue")

if __name__ == "__main__":
    window.run()
