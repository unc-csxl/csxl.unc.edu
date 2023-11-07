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

There are many different kinds of databases that we can use, however in COMP 423 and in the CSXL Web Application, we use a **PostGreSQL** relational database to store our data.

We can add this database component to our tech stack flowchart:

![Same flowchart as before but with PostGreSQL Database]()

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

**SQLAlchemy** is the primary SQL toolkit that we will use to interact with our PostGreSQL database. This tutorial will get you familiarized with SQLAlchemy and how it is used in the CSXL Application.

## Introduction to SQLAlchemy - Core and ORM

## SQLAlchemy Entities

### What are Entities?

As you know, our PostGreSQL database represents data in a _tabular format_ - meaning tables! As mentioned in the beginning, tables have columns (fields of data) and rows represent each entry in our data.

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

Remember, entities represent tables in our database. Let's say that I wanted to create an entity to represent the `organization` table of my PostGreSQL database.

First, recall that we said that we created `EntityBase` to serve as the _superclass_ of all of our entities. So, let's create an entity for our organization table that inherits from `EntityBase`.

```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"
```

First, notice that it is important to include the field `__tablename__`, spelled exactly in this way. This maps the entity (`OrganizationEntity`) to a table named `organization` in the PostGreSQL database.

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

## Connecting to the Database

### Creating the Session

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
