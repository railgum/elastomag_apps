from windows import Main_Window


window = Main_Window(700, 300, "Создание справки и сводной таблицы",
                     icon=None)
window.label.configure(
    text="@Автор программы - Раиль Гумеров.\nПриветствую вас в моем первом .exe-шном приложении!",
    fg="green"
)
window.entry.configure(width=50, fg="grey")

if __name__ == "__main__":
    window.run()
