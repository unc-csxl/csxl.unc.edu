# Get Started with Development

## Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [VSCode](https://code.visualstudio.com/)
* [VSCode DevContainers Extension](https://code.visualstudio.com/docs/devcontainers/containers)

## Before Starting a DevContainer: Establish a .env File

**You must complete this step _before_ attempting to start a VSCode DevContainer. If you do not, you will likely see the 'Open in DevContainer' action fail.**

The backend service configuration depends on [Environment Variables](https://12factor.net/config). Add the following contents to a file named `backend/.env` within the project:

```
MODE=development
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DATABASE=csxl
HOST=localhost
JWT_SECRET=REPLACE_ME
```

You should replace the value associated with `JWT_SECRET` with a randomly generated value, such as a [generated UUID](https://www.uuidgenerator.net/).

## Start the Dev Container

Use VSCode's Command Palette to run "Dev Container: Reopen in Container". This will kick-off a process that builds the development environment's container with most required dependencies, intialize a PostgreSQL database using the configuration defaults you specified in `.env`, and establish a special volume for the frontend's `node_modules` directory.

Once the Dev Container begins, open a terminal and complete the following:

1. Install frontend dependencies: 
    1. `pushd frontend` 
    2. `npm install`
    3. `popd`
2. Create database and reset demo data:
    2. `python3 -m backend.script.create_database`
    3. `python3 -m backend.script.reset_database`
3. Start dev server processes using the `honcho` process manager
    1. `honcho start`
        1. Wait until you see "frontend.1 | Compiled successfully" emitted from the Angular dev server.
    2. Open `localhost:1560` in a browser and you should see the XL site running locally in development.
    3. To stop the development servers, press `Ctrl+C` in the terminal running `honcho` and close VSCode.

## Develop in Branches

Before beginning any feature work, fixes, or other modifications, you should checkout a branch to keep the history separate from the `main` line history until it is ready deploying into production.

## Authorize as Alternate Users

When running in a development environment, it is helpful to be able to switch between authenticated users.
Our current mechanism for doing so is a special authorization route that only works in development:

Change users route pattern: `http://localhost:1560/auth/as/{onyen}/{pid}`

For reference, here are some mock personas that are installed in the `reset_database` script from above:

1. Sol Student: <http://localhost:1560/auth/as/sol/100000000>
2. Arden Ambassador: <http://localhost:1560/auth/as/arden/100000001>
3. Merritt Manager: <http://localhost:1560/auth/as/merritt/100000002>
4. Super User: <http://localhost:1560/auth/as/root/999999999>