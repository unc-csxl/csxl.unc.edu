# Connecting to the Database

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/16/2023_

## Preface

Now that you know a bit about SQLAlchemy and representing database table structures in SQLAlchemy Entities, let's learn how to actually connect to the database.

As you have seen in the stack flowchart, the backend _services_ are ultimately responsible for using SQLAlchemy to retreive data from the database. How can the service access SQLAlchemy?

We need to expose the **_session_** as an object that can be **_injected_** into each service so that we can use its functionality!

This idea is similar to how we inject frontend services into Angular components to use their functionality.

## Creating the Session

The code to handle the creation of the session is handled in `backend/database.py`, but let's take a look at what is going on in this code:

```py
import sqlalchemy
from sqlalchemy.orm import Session
from .env import getenv

def _engine_str(database=getenv("POSTGRES_DATABASE")) -> str:
    """Helper function for reading settings from environment variables to produce connection string."""

    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"


engine = sqlalchemy.create_engine(_engine_str(), echo=True)
"""Application-level SQLAlchemy database engine."""


def db_session():
    """Generator function offering dependency injection of SQLAlchemy Sessions."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
```

As you can see, there are three main components.

First, `_engine_str` reads your `.env` environment file to contain important information about how you are to access your database. This includes credentials such as our username and password, as well as the host and port by which we will connect to the database.

Then, we create an _engine_ based on these credentials. This engine allows us to interact with our SQL database.

Finally, we then create a `db_session` function that returns the **_SQLAlchemy Session_** - the object we will use to interact with our database in our services!

For example, let's take a look at the real `OrganizationService`!

```py
class OrganizationService:
    """Service that performs all of the actions on the `Organization` table"""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes the `OrganizationService` session."""
        self._session = session
```

The syntax `Depends()` in the initializer for the service allows us to use dependency injection! We can now access the shared `db_session` using the `_session` field.

We will use this session in Part 4 to interact with our database!
