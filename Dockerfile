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
FROM python:3.12 AS production

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /usr/local/bin/

# Create a non-root user
RUN groupadd --gid 1001 app && useradd --uid 1001 --gid app --create-home app

WORKDIR /workspace

COPY ./backend ./
COPY ./alembic.ini ./

WORKDIR /workspace/backend
RUN uv sync --all-packages --no-dev --no-editable && rm -rf /root/.cache

COPY --from=build /workspace/static/browser /workspace/static

WORKDIR /workspace
USER app
CMD ["/workspace/backend/.venv/bin/uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "3"]
ENV TZ="America/New_York"
EXPOSE 8080