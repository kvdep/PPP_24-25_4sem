FROM python:3.11.9-alpine

#ENV PYTHONPATH=/
WORKDIR /

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV PYTHONPATH=/app

CMD ["uvicorn", "main_celery:app", "--host", "0.0.0.0", "--port", "8001"]
# COPY . 3lab/app/celery/tasks.py

# если в docker-compose есть, следующую строку оставь закомментированной.
# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]