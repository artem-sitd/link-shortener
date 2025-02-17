# Используем официальный Python-образ
FROM python:3.12-slim

# Установим рабочую директорию
WORKDIR .

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта в контейнер
COPY . .

# Открываем порт для бота
EXPOSE 8080

# Запускаем бота
CMD ["python", "main.py"]
