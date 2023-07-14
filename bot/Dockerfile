FROM python:3.11-slim
WORKDIR /app_bot
RUN pip install poetry
COPY . / .
RUN poetry install
CMD ["poetry", "run", "python", "-m", "telegram_bot"]
