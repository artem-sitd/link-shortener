# 🔗 Telegram Link Shortener Bot

Telegram-бот для сокращения длинных URL-адресов. Пользователь отправляет боту длинную ссылку, в ответ получает короткий URL, который перенаправляет на исходный адрес. Проект развёртывается с использованием Docker Compose и включает в себя веб-сервер на FastAPI, Telegram-бота и Nginx.

---

## 🚀 Возможности

- 📩 Получение длинного URL от пользователя через Telegram
- 🔗 Генерация короткой ссылки и отправка её пользователю
- 🔁 Перенаправление по короткой ссылке на исходный URL
- 🐳 Развёртывание с использованием Docker Compose
- 🌐 Веб-сервер на FastAPI и Nginx

---

## 🧰 Технологии

- Python 3.10+
- FastAPI
- aiogram
- Nginx
- Docker & Docker Compose

---

## ⚙️ Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/artem-sitd/link-shortener.git
   cd link-shortener
   ```

2. **Настройте переменные окружения:**

   Переименуйте файл `.env.template` в `.env`:

   ```bash
   cp .env.template .env
   ```

   Отредактируйте файл `.env`, указав необходимые значения:

   - `TELEGRAM_API_KEY` — токен вашего бота, полученный у [@BotFather](https://t.me/BotFather)
   - `WEBHOOK_HOST` — публичный HTTPS-домен для вебхуков (например, с использованием [localtunnel](https://theboroer.github.io/localtunnel-www/))

3. **Установите localtunnel (для локального тестирования):**

   ```bash
   npm install -g localtunnel
   lt --port 8082
   ```

   Скопируйте предоставленный URL и вставьте его в переменную `WEBHOOK_HOST` в файле `.env`.

4. **Запустите приложение с помощью Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Приложение будет доступно по адресу `http://localhost:8082`.

---

## 📁 Структура проекта

```
├── app/                   # Основная логика приложения
├── .env.template          # Шаблон переменных окружения
├── docker-compose.yml     # Конфигурация Docker Compose
├── Dockerfile             # Docker-образ приложения
├── nginx.conf             # Конфигурация Nginx
├── main.py                # Точка входа в приложение
├── requirements.txt       # Зависимости проекта
├── settings.py            # Настройки приложения
└── README.md              # Документация проекта
```

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. файл `LICENSE`.
