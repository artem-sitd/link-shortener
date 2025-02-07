# Используем официальный Python-образ
FROM python:3.12-slim

# Установим рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для бота
EXPOSE 5000

# Запускаем бота
CMD ["python", "app/main.py"]
