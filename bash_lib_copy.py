import subprocess
import os
import tkinter as tk
from tkinter import filedialog
import shutil

def browse_file():
    """Открывает проводник и вставляет выбранный путь в Entry"""
    filepath = filedialog.askopenfilename(
        title="Выберите исполняемый файл"
    )

    if filepath:  # Если файл выбран (не нажата отмена)
        entry.delete(0, tk.END)  # Очищаем поле
        entry.insert(0, filepath)




def sucses_window():
    root2 = tk.Toplevel()

    root2.geometry("200x100")
    sucses_frame = tk.Frame(root2)
    sucses_frame.pack(expand=True, padx=5, pady=5)

    button = tk.Button(root2, text="Успешно", command=root2.destroy)
    button.place(relx=0.5, rely=0.7, anchor='center')




def error_window(argum):
    a_1 = argum

    root1 = tk.Toplevel()

    root1.geometry("500x200")
    error_frame = tk.Frame(root1)
    error_frame.pack(expand=True, padx=5, pady=5)

    label = tk.Label(root1, text="")
    label.pack(pady=20)

    messages = {
        "1": "Файл не является исполняемым",
        "2": "Файл не существует",
        "3": "Введите путь к файлу",
        "4": "Файл не является динамическим исполняемым"
    }

    error_type = messages.get(a_1)
    label.config(text=error_type)

    close_button = tk.Button(root1, text="Закрыть", command=root1.destroy)
    close_button.pack(pady=30)





def on_button_click():
    """Функция, которая вызывается при нажатии кнопки"""
    user_text = entry.get().strip()  # Получаем текст из поля ввода

    if not user_text:
        error_window("3")
        return
    elif not os.path.exists(user_text):
        error_window("2")
        return
    elif not os.access(user_text, os.X_OK):
        error_window("1")
        return
    result = subprocess.run(["ldd", user_text], capture_output=True, text=True)

    if result.returncode != 0:
        error_window("4")
        return

    lines = result.stdout.splitlines()
    paths = []
    missed_libs = []

    for line in lines:
        if '=>' in line:
            parts = line.split('=>')
            if len(parts) > 1:
                path = parts[1].strip().split()[0]
                if path != "not":
                    paths.append(path)
                else:
                    missed_libs.append(parts[0])
        elif line.strip().startswith('/'):
            path = line.strip().split()[0]
            paths.append(path)

    if missed_libs:
        with open("missed libs.txt", "w", encoding="utf-8")as file:
            for lib in missed_libs:
                file.write(lib.strip() + "\n")


    destination_folder = os.path.join(os.path.dirname(__file__), "libs")
    os.makedirs(destination_folder, exist_ok=True)

    for src_path in paths:
        shutil.copy(src_path, destination_folder)

    sucses_window()


root = tk.Tk()
root.title("")
root.geometry("450x250")  # Ширина x Высота

main_frame = tk.Frame(root)
main_frame.pack(expand=True, padx=5, pady=5)

# Поле ввода
entry_label = tk.Label(root, text="Исполняемый файл:")
entry_label.place(relx=0.5, rely=0.2, anchor='center')

entry = tk.Entry(root, width=22)
entry.place(relx=0.3, rely=0.4, anchor='center')

# Кнопка
button = tk.Button(root, text="Выполнить", command=on_button_click)
button.place(relx=0.5, rely=0.7, anchor='center')

browse_btn = tk.Button(root, text="Обзор...", command=browse_file)
browse_btn.place(relx=0.8, rely=0.4, anchor='center')

# Запускаем главный цикл
root.mainloop()