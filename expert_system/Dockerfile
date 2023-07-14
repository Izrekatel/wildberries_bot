FROM python:3.11-slim
WORKDIR /app_expert_system
RUN pip install poetry
COPY . / .
RUN poetry install
RUN apt-get update
RUN apt-get install postgresql-client -y
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "/app_expert_system/docker-entrypoint.sh" ]