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

If you see an error on your first attempt, retry once. If the error persists, double check that you have completed the `.env` file step above. The `.env` file must be located in the `backend` directory.

Once the Dev Container begins, open a terminal and complete the following:

1. Install frontend dependencies:
    1. `pushd frontend` 
    2. `npm install`
    3. `popd`
2. Reload the VS Code Window to ensure plugins are properly loaded:
    1. `Ctrl+Shift+P` to open the Command Palette
    2. Type "Reload Window" and select the action "Developer: Reload Window"
    3. It's unclear why this step is necessary, but it seems to fix issues with plugins initializing on first build of a DevContainer.
3. Create database and reset demo data:
    1. `python3 -m backend.script.create_database`
    2. `python3 -m backend.script.reset_demo`
4. Start dev server processes using the `honcho` process manager
    1. `honcho start`
        1. Wait until you see "frontend.1 | Compiled successfully" emitted from the Angular dev server.
    2. Open `localhost:1560` in a browser and you should see the XL site running locally in development.
    3. Try authorizing as Rhonda Root by visiting <http://localhost:1560/auth/as/rhonda/999999999> your browser.
    4. To stop the development servers, press `Ctrl+C` in the terminal running `honcho` and close VSCode.

## Development Data

You will notice the users and roles in your system are different than the production system. This is because the `reset_demo` script creates a set of mock users and roles for development purposes. Production data, with all registered users, contains protected information and is not directly replicable in a development environment. As new features are developed, additional demo and testing data can be added to the `reset_demo` and `reset_testing` scripts, respectively.

## Develop in Branches

Before beginning any feature work, fixes, or other modifications, you should checkout a branch to keep the history separate from the `main` line history until it is ready deploying into production. For students in COMP423, your final project `main` branch is called `stage`. As your projects are deployed separately from production, this is typically referred to as a "Staging" deployment / environment.

## Authorizing Alternate Users

When running in a development environment, it is helpful to be able to switch between authenticated users.
Our current mechanism for doing so is a special authorization route that only works in development:

Change users route pattern: `http://localhost:1560/auth/as/{onyen}/{pid}`

For reference, here are some mock personas that are installed in the `reset_testing` script from above:

1. Sally Student: <http://localhost:1560/auth/as/sally/111111111>
2. Larry CADS Leader: <http://localhost:1560/auth/as/larry/555555555>
3. Amy Ambassador: <http://localhost:1560/auth/as/amy/888888888>
4. Rhonda Root: <http://localhost:1560/auth/as/rhonda/999999999>