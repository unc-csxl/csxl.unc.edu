# SQLAlchemy Entities

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.
> _Last Updated: 11/16/2023_

## What are Entities?

As you know, our PostgreSQL database represents data in a _tabular format_ - meaning tables! As mentioned in the beginning, tables have columns (fields of data) and rows represent each entry in our data.

However, we need a way to actually _represent_ this database structure in Python. We can then use this structure to:

- Represent the expected shape of what our tables should look like, so if we were to _create database tables_ in our database, we can use the structure in Python as our guide.
- Represent data being read from the database as an object of this structure.

We call these structures **_SQLAlchemy Entities_**.

Entities fit into our overall stack flowchart like so:

![Stack flowchart zoomed in on the entities](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/images/sqlalchemy/entities.png)

## Creating Entities

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

## Entities vs. Pydantic Models

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
