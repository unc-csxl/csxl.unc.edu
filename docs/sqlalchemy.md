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

Now that we have access to the **_database session_** in our entity, how can we use it to perform CRUD operations?

CRUD operations are:

- **C**reate - Add new rows to the table
- **R**ead - Retrieve existing rows from the table
- **U**pdate - Modify existing rows on the table
- **D**elete - Remove rows from the table

You may remember this term from when you learned about APIs and HTTP request types. Here are how the request types match up to CRUD:

- **C**reate - `POST`
- **R**ead - `GET`
- **U**pdate - `PUT`
- **D**elete - `DELETE`

So, you may expect then, that `POST` APIs should call a function in the service that should perform a _create_ operation in our database. The `GET` API should call a function in the service that should perform a _read_ operation in our database, and so on.

### Transactions

In order for us to perform CRUD operations on our database, we must understand how these operations are performed. SQLAlchemy performs these operations using something called **_transactions_**. The purpose of a transaction is to denote an all-or-nothing collection of changes to a database. All-or-nothing refers to the fact that either _all_ of the requested changes should happen to the database. If something happens that would cause any change to fail, then _none_ of the changes are performed. This is incredibly vital for the integrity of the database. It ensures that the database is always in a consistent state even if errors occur, such as if a database modification fails, connection is dropped, in the middle of a transaction.

Consider the example used in class - transferring money between two bank accounts. Say that Kris Jordan bought his coworker, KMP, lunch. KMP wants to pay Kris Jordan back for $10. The following operations would be performed:

- `-$10` is removed from KMP's bank account
- `+$10` is added to Kris Jordan's bank account

In an ideal world, this transaction would occur and no issues would arise. But, what happened if, for example, there was a power outage in the middle of this transaction? One of four results could occur:

- KMP loses $10 and Kris Jordan gains $10, all is well.
- KMP loses $10 and Kris Jordan gains $0, meaning $10 disappeared!
- KMP loses $0 and Kris Jordan gains $10, meaning $10 spontaneouly appeared!
- Nothing happens.

For accounting purposes, the 2nd and 3rd scenarios are super bad. So instead, imagine that the two steps above (`-$10` and `+$10`) are \*bundled into one transaction.

Then, if the internet shuts off, the only two results could occur:

- KMP loses $10 and Kris Jordan gains $10, all is well.
- Nothing happens.

This eliminates the two worst outcomes! Either both statements are committed at the same time and the transaction succeeds, or neither is and the transaction gets "rolled back". When a rollback occurs, it's as if every statement earlier in the transaction is cancelled and never happened.

### Read Data

To read data from our database, we need to create a **query!**

A query is a request for data. Say that I want to read _all of the data_ from the organization table.

We can create a query to select the entire table using the `select` function of SQLAlchemy. Since we want to select the Organiztion table, and we know `OrganizationEntity` represents the organization table, we can pass that in, like so:

```py
from sqlalchemy import select

query = select(OrganizationEntity)
```

Now that we have this query (this request for data), we now need to act on this request! We can use the session to find all the rows (denotes as `scalars` here because they are one-dimensional units of data) that match this query:

```
self._session.scalars(query).all()
```

We then want to use `.all()` to ensure that we capture _all_ of the rows / scalars that match this query! So in this case, this will return all of the rows in the `organization` table.

What is the data type of this? Well, remember that SQLAlchemy entity objects represent data from the database. So, this result will be a list of entitites!

```py
query = select(OrganizationEntity)
entities = self._session.scalars(query).all()
```

Just like that, we have retrieved all the organization data from our database! We may put this in a service function called `OrganizationService.all()` that returns all of the organizations in our database. This would look like:

```py
class OrganizationService:

    def all(self) -> list[Organization]:
        query = select(OrganizationEntity)
        entities = self._session.scalars(query).all()

        return entities # uh-oh!
```

But, there is a problem here! Refer back to the full stack diagram. Remember that the service should be returning _Pydantic models_, **NOT entities!**

So, we would need to run a conversion:

```py
class OrganizationService:

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def all(self) -> list[Organization]:
        query = select(OrganizationEntity)
        entities = self._session.scalars(query).all()

        models = []
        for entity in entities:
            models.append(entity.to_model())

        return models
```

This looks good! This converts all of our entities to models.

But wait! There is actually a cool Python syntax trick to simplify this.

We can write this for loop:

```py
models = []
for entity in entities:
    models.append(entity.to_model())
```

as:

```py
models = [entity.to_model() for entity in entities]
```

This makes our code a lot more concise! The one line declaration can be summarized as follows:

```
final_list = [<what goes in .append()> for item in list]
```

So, our final `.all()` would look like:

```py
class OrganizationService:

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def all(self) -> list[Organization]:
        """Fetch all organizations from the database"""
        query = select(OrganizationEntity)
        entities = self._session.scalars(query).all()
        return [entity.to_model() for entity in entities]
```

Just like how we got _all_ of the data in our table, we can also get data from our table that matches a condition.

For example, what if I wanted to get only the public organizations from my database.

In this case, we need to use the query builder! Since we are doing more than just selecting the entire table, we need to use the `session.query()` function.

```py
entities = self._session.query(OrganizationEntity)
    .filter(OrganizationEntity.public == true)
    .all()
```

We pass in `OrganizationEntity` into `.query()` like we did with `select()`, but now we need to add a filter! This will append the filter condition to our query. We can filter our data for just when `OrganizationEntity.public == true`. Then, when we call `.all()`, the transaction runs and we get the data with the filter applied.

Our function might look something like:

```py
def all_public(self) -> list[Organization]:
    """Fetch all public organizations from the database"""
    entities = self._session.query(OrganizationEntity)
        .filter(OrganizationEntity.public == true)
        .all()
    return [entity.to_model() for entity in entities]
```

Lastly, we may want to query just _one_ element based on its _primary key_. SQLAlchemy includes a nifty helper function, `.get(__)`, for this purpose!

Recall that our `organization` example uses the `id` field as its primary key. What if we wanted to get an organization by its ID?

We can use:

```py
entity = self._session.get(OrganizationEntity, id)
```

Here, we just pass in the table / entity and then pass in the ID! Also notice that the result is just a single entity and not a list! `.get()` assumes you want at most one value to return.

So, we could create the function:

```py
def get_by_id(self, id: int) -> Organization:
    """Fetch an organization from the database based on its ID"""
    entity = self._session.get(OrganizationEntity, id)
    return entity.to_model()
```

### Write Data

Writing data to our database is pretty simple! To do this, we can use the `session.add()` function.

However, again - it is **_super important_** to rememebr which types we are working with! Our API will be calling this create function using a _Pydantic model_ request, and we must add an _entity_ to our database. So, we must convert an input model to an entity before we add it!

Say that in our service, we create a `.create()` function that takes in a new organization (Pydantic model) as a parameter:

```py
def create(self, organization: Organization) -> Organization:
    entity = OrganizationEntity.from_model(organization)
```

As you can see, we can use the `.from_model()` static method on the entity class to convert the model to the entity!

From there, we can add it to our transaction:

```py
def create(self, organization: Organization) -> Organization:
    entity = OrganizationEntity.from_model(organization)
    self._session.add(entity)
```

Two notes here! One is that SQLAlchemy is smart enough to know which table to add to since the entity corresponds to the right table. Second, we call `.add()`, _but not data is added yet!_ Why?

Remember what we talked about earlier with transactions! Since `.add()` mutates the state of the database, the `.add()` action is appended to the current transaction.

Think of this like _staging_ in Git! We are essentially adding all of the changes we want to be ready to be committed at once.

Just like Git, once we have created and completed our transaction, we execute it by calling `.commit()`.

Our final function would look like:

```py
def create(self, organization: Organization) -> Organization:
    entity = OrganizationEntity.from_model(organization)
    self._session.add(entity)
    self._session.commit() # Database is updated now.
    return entity.to_model()
```

Of course, if there is an error in the `.commit()` step, our transaction follows the _all-or-nothing_ principle that we discussed earlier.

You may also notice the `return` statement at the bottom! We return the object that we created (in model form) to ensure that it has been created correctly. There are also some instances where if we did not populate certain fields, the returned value would have those fields populated. This may be due to the `default=` rules defined earlier in the entity.

### Delete Data

Deleting data from our database is also extremely easy! Just like how the session as the `.add()` function, the session also has `.delete()`. The `.delete()` function takes in the object / row that should be deleted from the database.

Let's recall the function that we used to _get_ an organization by an ID:

```py
def get_by_id(self, id: int) -> Organization:
    """Fetch an organization from the database based on its ID"""
    entity = self._session.get(OrganizationEntity, id)
    return entity.to_model()
```

What if I wanted to modify this to delete an object by ID? Well, we only need to add two lines:

```py
def delete_by_id(self, id: int):
    """Delete an organization by ID"""
    entity = self._session.get(OrganizationEntity, id)
    self._session.delete(entity)
    self._session.commit() # Database is updated now.

```

This deletion follows the same _all-or-nothing_ principle as our `.create()` function did.

## Database Relationships

It is important to remember that data in your application does not exist in isolation. Many pieces of data are _related_ to each other!

Let's take the following example. Say that every UNC Computer Science organization, modeled by `Organization`, has one President that is unique to it (and for the sake of argument, assume that a person can only be President of one club at a time). Imagine that we were to model this President using `User`. Say that a user **Larry** is the president of a club called the **FORTRAN Development Club**.

Imagine how we may begin to represent this in our database tables. We are now looking to utilize the most powerful feature of _relational databases_ like PostgreSQL - support for relationships between tables.

First, let's examine the three different types of relationships:

### One-to-One Relationship

A **one-to-one relationship** is simply that one entry in one table can be related to at most one entry in another table - and the entry in the other table can only be related to one entry in the original table.

The example above with **Larry** and the **FORTRAN Development Club** is a textbook example of a one-to-one relationship. FORTRAN Development Club has only one President, Larry - and Larry is the President of only one club, the FORTAN Development Club. _There can only be one President for a club, and one user can only be the President of at most one club._

We can model this using the diagram below:

![One-to-one relationship diagram]()

Using the `Organization` and `User` example above, we may expect the models to have the following fields:

`Organization`

- ...
- `president: User`: The President of the club

`User`

- ...
- `president_for: Organization?`: The club the user is President of

### One-to-Many Relationship

In contrast, a **one-to-many relationship** is slightly different. In this type of relationship, an item in one table may be related to many items in the other table, but items in the other table can only be related to one element in the original table.

Take the following example. Imagine we have an entity called `Event` that stored information about events hosted by CS organizations. In this example, an `Organization` (like CS+SG, for example) can host many organizations - even as many as one a week - however, each event _only has one hosting organization_.

We can model this using the diagram below:

![One-to-many relationship diagram]()

Using the `Organization` and `Event` example above, we may expect the models to have the following fields:

`Organization`

- ...
- `events: list[Event]`: All of the events hosted by the organization

`Event`

- ...
- `organization: Organization`: Organization hosting this event

As you can see, unlike the _one-to-one relationship_, one of these fields would be a **_list_**! This is because an `Organization` can be related to _many_ `Event`s, but an `Event` can only be related to one `Organization`.

### Many-to-Many Relationship

The last type of relationship that we have is a **many-to-many** relationship. In this type of relationship, an item in one table may be related to many items in the other table, and items in the other table can be related to many items in the original table!

Take the following example. Imagine we are trying to represent organization membership (i.e., what organizations that students are a part of). In this example, an organization has many members. However, users also can be part of many organization at the same time.

We can model this using the diagram below:

![One-to-many relationship diagram]()

Using the `Organization` and `User` example above, we may expect the models to have the following fields:

`Organization`

- ...
- `members: list[User]`: All of the organization's members

`User`

- ...
- `organizations: list[Organization]`: All the organizations the user is a part of.

As you can see, in this example, both fields are lists!

Many-to-many relationships pose a unique challenge with database table design, which we will discuss further in the next section.

### Modeling Relationships in the Entity

Now that you understand database relationships at a high level, how do we actually add these relationships to our tables?

There are different methods for how we model these relationships based on the relationship type, however the base premise is still the same.

Recall the role of the _primary key_ field in a database table. The primary key serves as the **unique identifier** for each row. For example, the `id` fields of `Organization` and `Event` may be their tables' respective primary keys. The `pid` field may be the primary key of the `User` table.

With this knowledge about primary keys, how might we establish a relationship between the `organization` and `event` tables?

Let's recall the current structures of these tables:

**`organization` Table**

| PK? | Column Name | Data Type | Description                                                                                         |
| --- | ----------- | --------- | --------------------------------------------------------------------------------------------------- |
| \*  | id          | `int`     | Unique identifier (primary key) for each organization.                                              |
|     | name        | `str`     | Name of the organization.                                                                           |
|     | slug        | `str`     | Lowercased abbreviation of the organization to be used in URLs.                                     |
|     | description | `str`     | Description of the organization.                                                                    |
|     | public      | `bool`    | Whether or not anyone can join the organization (in the case that there is an application process). |

**`event` Table**

| PK? | Column Name | Data Type | Description                                     |
| --- | ----------- | --------- | ----------------------------------------------- | --- |
| \*  | id          | `int`     | Unique identifier (primary key) for each event. |
|     | name        | `str`     | Name of the event.                              |     |
|     | description | `str`     | Description of the event.                       |

How might we add a **_host organization_** to the events table?

Well, in our table schema, we can add a column for this! But, what would the value in this row be?

Remember, we said that primary keys uniquely identify items in a table! So, what if we added the _organization ID_ of the host organization to our `event` table? The result would look like this:

| PK? | Column Name     | Data Type | Description                                     |
| --- | --------------- | --------- | ----------------------------------------------- |
| \*  | id              | `int`     | Unique identifier (primary key) for each event. |
|     | name            | `str`     | Name of the event.                              |
|     | description     | `str`     | Description of the event.                       |
|     | organization_id | `int`     | ID of the hosting organization.                 |

We can then say that `organization_id` is a **_relationship field_** and directly points to the _primary key_ of the `organization` table.

How might we show this in our entity?

Let's look at our sample event entity:

```py
class EventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Event` table"""

    __tablename__ = "event"

    # Fields

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    description: Mapped[str] = mapped_column(String)
```

Adding a _relationship field_ to our entity is a a bit different than adding any normal field.

```py
organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
```

Above would be the correct way to declare the relationship field. Notice that instead of passing in a SQLAlchemy data type, we pass in a `ForeignKey()` object, and in its constructor, we pass in the field that this relates to.

In this case, since we want the event's `organization_id` field to relate to the organization's `id` field, we pass in `"organization.id"`, using the format `"tablename.field"`.

This is great! Now, we have established a relationship.

However, there is one problem with this convention. Say that we query data from the `Event` table. The result of this data would be `EventEntity` objects. What if I wanted to access the name of the event's hosting organization? Well, we could try:

```py
my_event.organization_id # uh oh
```

Notice that only the ID field is accessible! Now, in order to access my organization, I need to run an entirely new transaction:

```py
org_name = organization_service.get(my_event.organization_id)
```

This is not good or efficient! What if we can add a new property to our entity that would _store_ the related organization?

We actually can!

Take a look at the following completed entity implementation below:

```py
class EventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Event` table"""

    __tablename__ = "event"

    # Fields

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    description: Mapped[str] = mapped_column(String)

    # Relationships
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    # NEW
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")
```

You can see that this new field is of type `OrganizationEntity`! You may be wondering why it is in quotes in this example. Unfortunately, this is a quirk with the current version of SQLAlchemy and Python. Just note that this is roughly equivalent to how you would expect `Mapped[OrganizationEntity]` to function.

Since this field is not actually a column of this database, instead of setting this equal to a `mapped_column`, we can set it equal to a `relationship()` object.

You may also be wondering what `back_populates="events"` means?

Remember, a relationship is a two-way street. Just like how we added this `organization` field, we can add a similar field to our `OrganizationEntity` so that we can store all of the events that it hosts! This would be done like so:

```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"

    # Fields

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    description: Mapped[str] = mapped_column(String)

    public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships

    # NEW
    events: Mapped[list["EventEntity"]] = relationship(
            back_populates="organization", cascade="all,delete"
    )
```

Notice that `events` now stores the _list_ (because this is a one-to-many relationship) of all events that the organization hosts!

With this in mind, we can re-examine `back_populates`. We set this parameter _equal to the name of the relationship field in the other entity_. So:

- In `EventEntity`, we used `back_populates="events"`, because `events` was the field in the `OrganizationEntity.`
- In `OrganizationEntity`, we used `back_populates="organization"` because `organization` was the field in the `EventEntity`.

> NOTE: Also notice the `cascade="all,delete"` directive in the `OrganizationEntity`. This directs SQL to **_delete all related events_** when the organization is also deleted.
>
> This makes sense, because say we delete the _App Team_ organization, we also want to delete all relevant events (because all events must have a host organization, and deleting the host organization leaves orphaned events).

We can use these relationship fields to easily establish _one-to-one_ and _one-to-many_ relationships between our entities, as well as making our lives easier to access related elements!

To close out of the example from above, I would now be able to easily acess the name of hosting organization of an event, like so:

```py
org_name = my_event.organization.name
```

However, this convention is not so easily applied to _many-to-many relationships_.

### Join Tables

As mentioned in the last two previous sections, modeling _many-to-many relationships_ offers its own challenges.

### Resolving Model Circularity

## Further Reading

< database.md >
