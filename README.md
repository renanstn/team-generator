# team-generator

[![Python](https://img.shields.io/badge/python-%2314354C.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat&logo=nginx&logoColor=white)](https://www.nginx.com/)
[![GitHub Actions](https://img.shields.io/badge/githubactions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)](https://github.com/features/actions)

[![Lint Markdown](https://github.com/renanstn/team-generator/actions/workflows/markdown-lint.yaml/badge.svg)](https://github.com/renanstn/team-generator/actions/workflows/markdown-lint.yaml)
[![Lint Dockerfile](https://github.com/renanstn/team-generator/actions/workflows/dockerfile-lint.yaml/badge.svg)](https://github.com/renanstn/team-generator/actions/workflows/dockerfile-lint.yaml)
[![Pylint](https://github.com/renanstn/team-generator/actions/workflows/python-lint.yml/badge.svg)](https://github.com/renanstn/team-generator/actions/workflows/python-lint.yml)
[![Test Backend](https://github.com/renanstn/team-generator/actions/workflows/test-backend.yaml/badge.svg)](https://github.com/renanstn/team-generator/actions/workflows/test-backend.yaml)

## Objetivos

- Permitir abrir um evento para que as pessoas se inscrevam;
- Permitir que um usuário se inscreva em um evento;
- Permitir que um administrador dispare a ação de gerar times;
- Permitir a impressão da lista de times em PDF.

## Desenvolvimento

### Stack

- Backend
    - Poetry
    - FastAPI
    - Uvicorn
    - Reportlab
    - Postgres
- Frontend
    - Vue 3
    - Element plus

### Setup

Suba o projeto todo com o comando:

```sh
docker-compose up
```

Acesse:

- `http://localhost:5173`

A documentação da API ficará disponível em:

- `http://localhost:8000/docs`

Caso queira visualizar os dados brutos no banco de dados, você pode utilizar o
**Adminer**, que fica disponível em:

- `http://localhost:8080`

### Testes unitários

```sh
docker-compose run --rm --no-deps api pytest
```
