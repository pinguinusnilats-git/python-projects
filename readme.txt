# ELF Dependency Extractor

Простое GUI-приложение на Python/Tkinter.
Берёт ELF-исполняемый файл, проверяет его зависимости через `ldd`, копирует найденные библиотеки в папку `./libs`, а отсутствующие пишет в `missed_libs.txt`.

## Запуск
```bash
python app.py