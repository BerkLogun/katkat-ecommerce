FROM python:3.8-slim



ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
      build-essential libpq-dev git \
      && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      "uvicorn[standard]" \
      gunicorn \
      psycopg2-binary \
      django==3.2.24 \
      django-cors-headers==3.14.0

COPY tenant_router.py /app/tenant_router.py
COPY settings_poc.py  /app/settings_poc.py
COPY django_project/ /app/django_project/

ENV DJANGO_SETTINGS_MODULE=settings_poc

CMD ["gunicorn", "django_project.asgi:application", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"] 