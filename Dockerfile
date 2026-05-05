FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Entrypoint — устанавливаем права до смены пользователя
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Создаём непривилегированного пользователя и нужные папки с правами
RUN useradd --create-home django \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

# Копируем исходный код
COPY --chown=django:django . .

USER django

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
