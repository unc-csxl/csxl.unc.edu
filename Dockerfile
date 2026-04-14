# Front-end Build Steps
FROM node:22 as build
COPY ./frontend/package.json /workspace/frontend/package.json
COPY ./frontend/pnpm-lock.yaml /workspace/frontend/pnpm-lock.yaml
COPY ./frontend/angular.json /workspace/frontend/angular.json
WORKDIR /workspace/frontend
RUN corepack enable \
	&& corepack prepare pnpm@10.17.1 --activate
RUN pnpm install --frozen-lockfile
ENV SHELL=/bin/bash
RUN ng analytics disable
COPY ./frontend/src /workspace/frontend/src
COPY ./frontend/*.json /workspace/frontend
RUN node --max-old-space-size=1024 ./node_modules/@angular/cli/bin/ng build --optimization --output-path ../static

# Back-end Build Steps
FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /usr/local/bin/
COPY ./backend/pyproject.toml /workspace/backend/pyproject.toml
COPY ./backend/uv.lock /workspace/backend/uv.lock
WORKDIR /workspace/backend
RUN uv sync --frozen --no-dev --link-mode=copy
WORKDIR /workspace
COPY --from=build /workspace/static/browser /workspace/static
COPY ./backend /workspace/backend
COPY ./alembic.ini /workspace/alembic.ini
CMD ["uv", "run", "--project", "/workspace/backend", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "3"]
ENV TZ="America/New_York"
EXPOSE 8080