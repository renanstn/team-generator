# Base ------------------------------------------------------------------------
FROM python:3.9 AS base

WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY pyproject.toml poetry.lock /app/
RUN pip install --no-cache-dir poetry==1.6.1 && \
    poetry config virtualenvs.create false

# Development -----------------------------------------------------------------
FROM base AS development

RUN poetry install
COPY . /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production ------------------------------------------------------------------
FROM base AS production

RUN poetry install --without dev
COPY . /app/
RUN chmod +x start-production.sh
CMD ["start-production.sh"]
