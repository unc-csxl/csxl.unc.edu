# SQLAlchemy Tutorial

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/6/2023_

## Preface

Throughout this course so far, you have been learning about each layer of the tech stack. You started in the frontend, with _Angular components_ - what the users see on each page. You then moved downwards to the _Angular services_, which help to fetch and update data for your application. You then began to explore the backend layer, using _FastAPI_ to expose data across HTTP to your frontend services. Lastly, you made it to the _backend service_ layer, which your APIs called to in order to manipulate data. These layers can be represented using this flowchart:

![Flowchart 1 showing everything except the ORM session and PostGres]()

All of the layers you have been exposed to so far have enabled you to create extremely powerful web applications. However, there is one problem.

**_Your data does not save._**

You probably encountered this issue already. You refresh your page or restart your project, and all of the data that you worked with disappeared. In the real world, this is not the case. How many times have you gone onto Instagram and seen all of your photos disappear?

_This indicates that something is missing in our stack._

We are missing a place to _store data_ such that it **persists** - or, is _saved_ forever. We need a durable container that stores our data such that whether we refresh the page, restart our project, or update our live deployment (on CloudApps), our data remains in tact.

**Enter the database!**

The database is the core component of the _final layer of our COMP 423 tech stack_ - the **persistent data store**. The database is the durable container mentioned earlier that will keep our data in tact.

There are many different kinds of databases that we can use, however in COMP 423 and in the CSXL Web Application, we use a **PostgreSQL** relational database to store our data.

We can add this database component to our tech stack flowchart:

![Same flowchart as before but with PostgreSQL Database]()

Relational databases store data in _tables_. Each table has rows and columns, where each column represents a field of data and has a distinct data type. Rows represent an entry of data. Each row often as a primary key, or unique identifier or value that is used to easily identify it. For example, this may be a sample table for users within the CSXL application:

**Table `user`**

| PID (\*)  | name          | ONYEN      |
| --------- | ------------- | ---------- |
| 111111111 | Sally Student | `sstudent` |
| 999999999 | Rhonda Root   | `rroot`    |

In this case, we have three fields:

- `PID (*)`: This is our primary key, denoted by the star. It is unique to each individual and can be used to identify a row; data type integer.
- `name`: The name of the individual; data type string.
- `ONYEN`: The ONYEN of the individual; data type string.

In order to interact with a relational databases, we use **SQL** _(Structured Query language)_. We can use SQL to store and process information within a database.

For example, if I wanted to grab every entry of the `user` table using SQL:

```sql
SELECT * FROM user
```

Note the `*` here means that I am selecting all the columns from the `user` table. If I wanted to grab a user with the PID `999999999`:

```sql
SELECT * FROM user WHERE pid=999999999
```

Of course, this is super cool! However, there is a problem. It is quite hard to write and execute pure SQL queries in Python. Plus, there is a lot of things behind the scenes to manage here. We need a tool that allows us to connect to our SQL database from Python so that we can manage the data in our database.

**Enter SQLAlchemy!**

**SQLAlchemy** is the primary SQL toolkit that we will use to interact with our PostgreSQL database. This tutorial will get you familiarized with SQLAlchemy and how it is used in the CSXL Application.

## Introduction to SQLAlchemy - Core and ORM

## SQLAlchemy Entities

### What are Entities?

As you know, our PostgreSQL database represents data in a _tabular format_ - meaning tables! As mentioned in the beginning, tables have columns (fields of data) and rows represent each entry in our data.

However, we need a way to actually _represent_ this database structure in Python. We can then use this structure to:

- Represent the expected shape of what our tables should look like, so if we were to _create database tables_ in our database, we can use the structure in Python as our cide.
- Represent data being read from the database as an object of this structure.

We call these structures **_SQLAlchemy Entities_**.

Entities fit into our overall stack flowchart like so:

![Stack flowchart zoomed in on the entities]()

### Creating Entities

The SQLAlchemy ORM contains the basic building blocks for us to create entities, and these tools are made available in the `DeclarativeBase` class of the ORM. We can import it like so:

```py
from sqlalchemy.orm import DeclarativeBase
```

From here, we can create one class that can act as a superclass for all of our models. This class will also inherit from `DeclarativeBase` to have access to all of the necessary features that will make it an entity. We can declare this like so:

```py
class EntityBase(DeclarativeBase):
    pass
```

Notice that this class is essentially empty! It just inherits everything from `DeclativeBase`.

**_From here,_** we can create SQLAlchemy entities!

Remember, entities represent tables in our database. Let's say that I wanted to create an entity to represent the `organization` table of my PostgreSQL database.

First, recall that we said that we created `EntityBase` to serve as the _superclass_ of all of our entities. So, let's create an entity for our organization table that inherits from `EntityBase`.

```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"
```

First, notice that it is important to include the field `__tablename__`, spelled exactly in this way. This maps the entity (`OrganizationEntity`) to a table named `organization` in the PostgreSQL database.

Now from here, we can add our fields - what will be _columns_ in our database.

Let's think about the columns that we may want in our `organization` table. Below are a few examples.

| PK? | Column Name | Data Type | Description                                                                                         |
| --- | ----------- | --------- | --------------------------------------------------------------------------------------------------- |
| \*  | id          | `int`     | Unique identifier (primary key) for each organization.                                              |
|     | name        | `str`     | Name of the organization.                                                                           |
|     | slug        | `str`     | Lowercased abbreviation of the organization to be used in URLs.                                     |
|     | description | `str`     | Description of the organization.                                                                    |
|     | public      | `bool`    | Whether or not anyone can join the organization (in the case that there is an application process). |

_Note: PK denotes "primary key"._

It is important to note that, when we create entities, we are **mapping** Python fields to a SQL relational database column. To establish this mapping, we use the following syntax from SQLAlchemy to define fields in our entity:

```py
field_name: Mapped[<python_type>] = mapped_column(<SQLDataType>)
```

In this example, `mapped_column()` is a function from the SQLAlchemy ORM that establishes this column.

The Python type is the data type of what data we want to represent in Python. This could be common types as written in the table above, such as `int`, `str`, and `bool`.

However, SQL relational databases have their own corresponding types. SQLAlchemy includes these types and makes them importable. For example:

- `str` maps to `String`
- `int` maps to `Integer`
- `bool` maps to `Boolean`

So, using the code above and including new import statements, let's create our entity based on the data above!

```py
# Import our mapped SQL types from SQLAlchemy
from sqlalchemy import Integer, String, Boolean
# Import mapping capabilities from the SQLAlchemy ORM
from sqlalchemy.orm import Mapped, mapped_column
# Import the EntityBase that we are extending
from .entity_base import EntityBase

class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"

    # Fields

    # Unique ID for the organization
    # NOTE: Notice the `primary_key=True` to denote that this is a primary key.
    # NOTE: Also notice the `autoincrement=True`. This allows our IDs to be automatically populated in increasing order as we add more organizations to our table.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Name of the organization
    # NOTE: Notice `nullable=False`. This indicates that this column cannot be blank - there must be a value here. If none is provided, it defaults to "" because of `default=""`.
    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    # Description of the organization
    description: Mapped[str] = mapped_column(String)

    # Whether the organization can be joined by anyone or not
    public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

```

There you have it, we have now created an entity! This entity provides the structure for the `organization` table and also serves as a data type for data that we directly retrieve from the table.

### Entities vs. Pydantic Models

If you examined the tech stack diagram closely, or referred to previous exercises in class, you are probably getting a bit confused and thinking,

_I already created objects to represent my data in Python - my models! Why do I need entities too?_

This is a great question - and an extremely important point. Let's recall the purpose of Pydantic models.

Pydantic models:

- Represent the shape of data transferred by the _backend's API_.

In contrast, SQLAlchemy entities:

- Represent the shape of data used by the _PostgreSQL database_.

This difference is actually quite notable! There are cases where what data the API exposes and what data is stored in the database are different from one another. Therefore, it is important that we separate these two items.

Let's take a look at the interactions again using the flowchart:

![Compare Pydantic models from the SQLAlchemy entities]()

FastAPI only works with Pydantic models, and the SQLAlchemy session only works with Entities. Because of this, we will need to **convert\*** SQLAlchemy entitites to Pydantic models and vice-versa. As you can see in the flowchart, the service sits in the middle of FastAPI and the session. Therefore, **_it is the job of the service to make these conversions!_**

In order for the service to make these conversions, there must be helper functions that it can call. We can define these helper functions in the SQLAlchemy entities.

First, we need a method to convert entities to models. We can call this `.to_model()`, and here is a sample declaration:

**In the entity:**

```py
class OrganizationEntity(EntityBase):

    ...

    def to_model(self) -> Organization:
        """
        Converts a `OrganizationEntity` object into a `Organization` model object

        Returns:
            Organization: `Organization` object from the entity
        """
        return Organization(
            id=self.id,
            name=self.name,
            description=self.description,
            public=self.public,
        )
```

**Example Usage:**

```py
my_model: Organization = my_entity.to_model()
```

As you can see, this function is pretty simple! It just returns an `Organization` model object based on the fields in our entity.

We also need a function to convert a model back to an entity. We can make this a **_static method_** on the `OrganizationEntity` class with the name `.from_model(model)`, so we can call this using `OrganizationEntity.from_model(a_model)`. In Python, we declare static methods using the `@classmethod` decorator. Here is an example:

```py

class OrganizationEntity(EntityBase):

    ...

    def to_model(self) -> Organization:
        # Implementation hidden

    @classmethod
    def from_model(cls, model: Organization) -> Self:
        """
        Class method that converts an `Organization` model into a `OrganizationEntity`

        Parameters:
            - model (Organization): Model to convert into an entity
        Returns:
            OrganizationEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            public=model.public
        )
```

In Python, `cls` is automatically passed in as the first parameter for class methods and refers to the class that the static method is acting on. So in thie case, `cls` is referring to the `OrganizationEntity` class. So, this is returning an object of type `OrganizationEntity`.

**Example Usage:**

```py
my_entity: OrganizationEntity = OrganizationEntity.from_model(my_model)
```

Together, these functions allow the conversion from entites to models and back!

I encourage you to take a look at the following files:

- `backend/entities/organization_entity.py`
- `backend/services/organization.py`

The first file shows the _real_ SQLAlchemy entity for organizations used in the CSXL application! There are a few more fields, but the structure is still the same. Feel free to take a look at the `to_model()` and `from_model()` functions too!

The second file is the service, which as we talked about before, should be converting between models and entities! We can see that the service does this perfectly and utilizes the `to_model()` and `from_model()` as defined in the entity.

## Connecting to the Database

Now that you know a bit about SQLAlchemy and representing database table structures in SQLAlchemy Entities, let's learn how to actually connect to the database.

As you have seen in the stack flowchart, the backend _services_ are ultimately responsible for using SQLAlchemy to retreive data from the database. How can the service access SQLAlchemy?

We need to expose the **_session_** as an object that can be **_injected_** into each service so that we can use its functionality!

This idea is similar to how we inject frontend services into Angular components to use their functionality.

### Creating the Session

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

We will use this session in the next section.

## CRUD Operations

### Transactions

### Read Data

### Write Data

### Delete Data

## Database Relationships

### One-to-One Relationship

### One-to-Many Relationship

### Many-to-Many Relationship

### Modeling Relationships in the Entity

## Modelling Your Data

### Designing Database Tables

### Relationships

### Join Tables

### Resolving Model Circularity

## Further Reading

< database.md >
