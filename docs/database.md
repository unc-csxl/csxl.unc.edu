# Database Documentation

This project uses PostgreSQL for its data persistence tier.

## Development Concerns

One of the key design goals of database concerns in our development environment is that it is stress-free to completely reset its state back to a working baseline. This means you can delete the entire database directly, and recreate it, or merely just reset its data, in a scripted way.

The development container's `.devcontainer/docker-compose.yml` file specifies the `db` service based on the official `postgres:15.2` Docker Hub image. Its configuration settings are specified in environment variables in the `backend/.env` directory.

By convention, our development database's environment settings are:

~~~
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DATABASE=csxl
~~~

### Creating a Database

The development script to create the `csxl` database in PostgeSQL is in `backend/script/create_database.py`

To execute the script: `python3 -m backend.script.create_database`

### Deleting the Database

In development, when table schema and relationships are changing, you may run into scenarios where foreign key constraints are violated when tables are attempted to be dropped. This is especially true when you are iterating on the design of relationships (column names, etc). The easiest resolution is simply to delete the database in its entirety and recreate it.

The development script to delete the `csxl` database in PostgreSQL is in `backend/script/delete_database.py`

To execute the script: `python3 -m backend.script.delete_database`

To create the database, as discussed in the previous section, `python3 -m backend.script.create_database`

Finally, complete the steps below to reload development data into the database.

### Resetting the Database's Data

There are two scripts for loading database data: 

#### 1. Reset to Demo Data

When giving a demonstration of a feature and interacting with it, it's often helpful to have ample rows of data pre-loaded into the system to give a real sense from the user's perspective of what working with this feature will feel like in production. This is still synthetic, dummy data that is not truly reflective of production data but it _demos_ more realistically than purely testing data.

As an example, for student organizations, the demo data script will load all active student organizations as of start of Fall 2023. However, the testing data reset (below) will only load a small subset of them for automated testing purposes.

To reset your development environment with demo data: `python3 -m backend.script.reset_demo`

#### 2. Reset to Testing Data

When writing integration tests of backend services with the database, we establish a database with minimal data loaded into it for testing purposes. This data is kept minimal because all of this data is deleted and reloaded _for every single integration test_ in our test suite.

We make it possible to load the data from our integration test suite into the development environment for two reasons, first, to let you see what the test data looks like from the running application, and second, so that you can access the test data from the PostgreSQL data viewer, described below, in the event that your tests are behaving in a surprising fashion and need to confirm the data that resides in the database at the start of testing.

To reset your development environment with testing data: `python3 -m backend.script.reset_testing`

### Using PostgreSQL Viewer (VSCode Plugin)

* The VSCode PostgreSQL Extension by Chris Kolkman works well for viewing database tables and queries
* Open the Tool from Sidebar
* First time connecting? Add a connection to the database!
    1. From VSCode Command Palette- PostgreSQL: Add Connection 
    2. Add the connection using the environment settings above:
        * Hostname: `db`
        * Username: `postgres`
        * Password: `postgres`
        * Port: `5432`
        * Connection: `Standard`
        * Database: `csxl`
        * Display Name: `db`
* Common uses:
    * Expand a table to see its columns
    * Right click a table to run a query (such as selecting first 1000 rows)