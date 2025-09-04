import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog


def browse_file():
    """Открывает диалог выбора файла и вставляет путь в поле ввода."""
    filepath = filedialog.askopenfilename(title="Выберите исполняемый файл")

    if filepath:  # Если файл выбран (не нажата отмена)
        entry.delete(0, tk.END)
        entry.insert(0, filepath)


def success_window():
    """Окно с уведомлением об успешном завершении."""
    root2 = tk.Toplevel()
    root2.geometry("200x100")

    tk.Label(root2, text="Завершено успешно!").place(relx=0.5, rely=0.3, anchor="center")

    button = tk.Button(root2, text="Ок", command=root2.destroy)
    button.place(relx=0.5, rely=0.7, anchor="center")


def error_window(error_code: str):
    """Показывает окно с ошибкой по коду."""
    messages = {
        "1": "Файл не является исполняемым",
        "2": "Файл не существует",
        "3": "Введите путь к файлу",
        "4": "Файл не является динамическим исполняемым",
    }

    root1 = tk.Toplevel()
    root1.geometry("500x200")

    label = tk.Label(root1, text=messages.get(error_code, "Неизвестная ошибка"))
    label.pack(pady=20)

    close_button = tk.Button(root1, text="Закрыть", command=root1.destroy)
    close_button.pack(pady=30)


def on_button_click():
    """Проверяет выбранный файл, ищет его зависимости и копирует их в папку ./libs."""
    user_text = entry.get().strip()

    # Проверки файла
    if not user_text:
        error_window("3")
        return
    if not os.path.exists(user_text):
        error_window("2")
        return
    if not os.access(user_text, os.X_OK):
        error_window("1")
        return

    # Проверяем ldd
    result = subprocess.run(["ldd", user_text], capture_output=True, text=True)
    if result.returncode != 0:
        error_window("4")
        return

    # Разбор вывода ldd
    lines = result.stdout.splitlines()
    paths: list[str] = []
    missed_libs: list[str] = []

    for line in lines:
        if "=>" in line:
            parts = line.split("=>")
            if len(parts) > 1:
                path = parts[1].strip().split()[0]
                if path != "not":
                    paths.append(path)
                else:
                    missed_libs.append(parts[0])
        elif line.strip().startswith("/"):
            path = line.strip().split()[0]
            paths.append(path)

    # Записываем отсутствующие библиотеки
    if missed_libs:
        with open("missed_libs.txt", "w", encoding="utf-8") as file:
            for lib in missed_libs:
                file.write(lib.strip() + "\n")

    # Копируем найденные библиотеки
    destination_folder = os.path.join(os.path.dirname(__file__), "libs")
    os.makedirs(destination_folder, exist_ok=True)

    for src_path in paths:
        try:
            shutil.copy(src_path, destination_folder)
        except Exception as e:
            print(f"Не удалось скопировать {src_path}: {e}")

    success_window()


if __name__ == "__main__":
    # Главное окно
    root = tk.Tk()
    root.title("Зависимости ELF")
    root.geometry("450x250")

    # Подпись
    entry_label = tk.Label(root, text="Исполняемый файл:")
    entry_label.place(relx=0.5, rely=0.2, anchor="center")

    # Поле ввода
    entry = tk.Entry(root, width=22)
    entry.place(relx=0.3, rely=0.4, anchor="center")

    # Кнопки
    button = tk.Button(root, text="Выполнить", command=on_button_click)
    button.place(relx=0.5, rely=0.7, anchor="center")

    browse_btn = tk.Button(root, text="Обзор...", command=browse_file)
    browse_btn.place(relx=0.8, rely=0.4, anchor="center")

    root.mainloop()

