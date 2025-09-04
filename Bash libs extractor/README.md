# ELF Dependency Extractor

GUI-приложение на Python/Tkinter.
Берёт ELF-исполняемый файл, проверяет его зависимости через `ldd`, копирует найденные библиотеки в папку `./libs`, а отсутствующие пишет в `missed_libs.txt`.

## 🚀 Установка и запуск
```bash
git clone https://github.com/yourname/elf-dependency-extractor
cd elf-dependency-extractor
python app.py

