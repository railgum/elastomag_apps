from windows import MainWindow


window = MainWindow(650, 300, "Создание справки и сводной таблицы",
                    icon="src/app_for_tk/img/icon.ico")
window.label.configure(
    text="@Автор программы - Раиль Гумеров",
    fg="green"
)
window.text.insert(
    "1.0", """Это моё первое .exe-шное приложение. О всех пожеланиях по работе программы, пожалуйста, напишите мне на почту:railbolo@gmail.com""")
window.text.configure(bg="SystemButtonFace",
                      state="disabled", bd=0, fg="purple", wrap="word")
window.entry.configure(width=50, fg="grey")

if __name__ == "__main__":
    window.run()
