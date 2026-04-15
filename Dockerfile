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

# Create a non-root runtime user while preserving OpenShift arbitrary-UID compatibility.
RUN useradd --uid 1001 --gid 0 --create-home --home-dir /home/app app
WORKDIR /workspace

COPY ./backend/pyproject.toml /workspace/backend/pyproject.toml
COPY ./backend/uv.lock /workspace/backend/uv.lock
WORKDIR /workspace/backend
RUN python -m venv /workspace/backend/.venv \
	&& VIRTUAL_ENV=/workspace/backend/.venv PATH="/workspace/backend/.venv/bin:$PATH" uv sync --frozen --no-dev --link-mode=copy --active \
	&& chmod -R a+rX /workspace/backend/.venv
ENV HOME="/home/app"
ENV VIRTUAL_ENV="/workspace/backend/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=build /workspace/static/browser /workspace/static
COPY ./backend /workspace/backend
COPY ./alembic.ini /workspace/alembic.ini
RUN chown -R 1001:0 /workspace /home/app \
	&& chmod -R g=u /workspace /home/app

USER 1001
WORKDIR /workspace
CMD ["/workspace/backend/.venv/bin/python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "3"]
ENV TZ="America/New_York"
EXPOSE 8080