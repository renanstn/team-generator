FROM python:3.9 AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code
RUN pip install --no-cache-dir poetry==1.4.2
COPY pyproject.toml poetry.lock /code/

FROM base AS development
RUN poetry config virtualenvs.create false && \
    poetry install
COPY . /code/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS production
RUN poetry config virtualenvs.create false && \
    poetry install --without dev
COPY . /code/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
