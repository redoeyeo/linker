# Используем официальный образ Python 3.12 как базовый
FROM python:3.14-slim

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем системные зависимости для Vosk и обработки аудио
RUN apt-get update
RUN apt-get install -y ffmpeg 

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml .

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root

# Копируем исходный код приложения
COPY app app

# Создаем директорию для моделей Vosk
RUN mkdir -p models


# Экспортируем переменную окружения для модели Vosk
ENV VOSK_MODEL_DIR=/app/models

# Открываем порт 8000
EXPOSE 8000


CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
