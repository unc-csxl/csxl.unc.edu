# Front-end Build Steps
FROM node:22 as build
COPY ./frontend/package.json /workspace/frontend/package.json
COPY ./frontend/pnpm-lock.yaml /workspace/frontend/pnpm-lock.yaml
COPY ./frontend/angular.json /workspace/frontend/angular.json
WORKDIR /workspace/frontend
RUN corepack enable \
	&& corepack prepare pnpm@10.17.1 --activate
RUN pnpm install --frozen-lockfile --ignore-scripts
ENV SHELL=/bin/bash
RUN pnpm exec ng analytics disable
COPY ./frontend/src /workspace/frontend/src
COPY ./frontend/*.json /workspace/frontend
RUN NODE_OPTIONS=--max-old-space-size=1024 pnpm exec ng build --optimization --output-path ../static

# Back-end Build Steps
# Back-end Build Steps
FROM python:3.11 AS production

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /usr/local/bin/

WORKDIR /workspace/backend

COPY ./backend/pyproject.toml ./pyproject.toml
COPY ./backend/uv.lock ./uv.lock

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_NO_MANAGED_PYTHON=1 \
    UV_PYTHON=python3 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    TZ=America/New_York

RUN command -v python3 \
    && python3 --version \
    && uv sync --frozen --no-dev

WORKDIR /workspace

COPY --from=build /workspace/static/browser /workspace/static
COPY ./backend /workspace/backend
COPY ./alembic.ini /workspace/alembic.ini

RUN chgrp -R 0 /workspace /opt/venv /tmp \
    && chmod -R g=u /workspace /opt/venv /tmp

USER 1001
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "3"]
EXPOSE 8080