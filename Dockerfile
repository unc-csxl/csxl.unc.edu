# Front-end Build Steps
FROM node:18 as build
COPY ./frontend/package.json /workspace/frontend/package.json
COPY ./frontend/angular.json /workspace/frontend/angular.json
WORKDIR /workspace/frontend
RUN npm install -g @angular/cli && npm install
ENV SHELL=/bin/bash
RUN ng analytics disable
COPY ./frontend/src /workspace/frontend/src
COPY ./frontend/*.json /workspace/frontend
RUN ng build --optimization --output-path ../static

# Back-end Build Steps
FROM python:3.11
RUN python3 -m pip install --upgrade pip
COPY ./backend/requirements.txt /workspace/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/backend/requirements.txt
COPY --from=build /workspace/static /workspace/static
COPY ./backend /workspace/backend
WORKDIR /workspace
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
ENV TZ="America/New_York"
EXPOSE 8080