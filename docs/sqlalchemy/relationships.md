# Database Relationships

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>
> *Last Updated: 11/14/2023*

It is important to remember that data in your application does not exist in isolation. Data in one table of your database may need to point to other data in other tables.

Let's take the following example. Say that every UNC Computer Science organization is stored in a SQL table defined by the `OrganizationEntity`. Assume that you have just received a ticket asking you to keep track of each organization's President in your database. This data will eventually be used to display the name of organizations' Presidents on each organization detail page.

You have been told that, for the purposes of this ticket, you are to assume that each Organization has a single President unique to it, and that a user can be a President of at most one club. 

Given this information, you assume that you need to work with two of your tables in the PostgreSQL database - the `organization` and `user` tables. You also know that these tables are defined by the `OrganizationEntity` and `UserEntity` entities respectively. These two entities are separate, so how would be make this connection? We are now looking to utilize the most powerful feature of _relational databases_ like PostgreSQL - support for _relationships_ between tables.

***Database relationships*** define the connections between tables in a database and allow for tables to reference other tables. In this case, we want organizations found in the `organizations` table to be able to *refer to / point to* users in the `user` table - specifically, the user that is its President.

## Types of Database Relationships

There are three main types of database relationships: *one-to-one*, *one-to-many*, and *many-to-many* relationships.

| Relationship | Description | Example                                                                                           |
| -----------  | --------- | --------------------------------------------------------------------------------------------------- |
| One to One   | Each item in one table points to at most one item in another table, and vice-versa. | We can represent organizations and their Presidents using a one-to-one relationship. Each organization has only one President, and each user can be the President of at most one club. |
| One to Many  | Each item in one table points to many items in another table, but items in the other table can point to at most one item in the original table.     | We can represent organizations and events they host using a one-to-many relationship. Each organization can host numerous events, but each event is hosted primarily by one organization. |
| Many to Many | Each item in one table can point to many items in another table, and vice-versa.    | We can event event registrations as a many-to-many relationship. Each event can have many registered users, and users can also register for many events at once. |

As you can see based on the descriptions of the different types of relationships, our Organization and President example is best realized using a one-to-one relationship. It is extremely important to carefully think through the feature you are trying to add and which type of relationship you will need to successfully model your data. Depending on the relationship you want to establish, you will need to modify your SQLAlchemy entities differently.

Below, I am going to discuss each example in the "Example" column in the table and how you would need to modify your entities to include all three types of relationships.

## Implementing a One-to-One Relationship

### Background

The example from the beginning, where we are attempting to relate the `organization` and `user` tables together to store the President of each organization, is a textbook example of a one-to-one relationship.

Below is a good representation of some of the important fields of `organization` and `user` tables, defined in the `OrganizationEntity` and `UserEntity` classes respectively:

----
**`OrganizationEntity` Fields (columns in the `organization` table)**

| PK? | Column Name | Data Type | Description                                                                                         |
| --- | ----------- | --------- | --------------------------------------------------------------------------------------------------- |
| `*`  | id          | `int`     | Unique identifier (primary key) for each organization.                                              |
|     | name        | `str`     | Name of the organization.                                                                           |
|     | ...         | *various*     | *Many more specific organization fields are hidden here.*                                       |

----
**`UserEntity` Fields (columns in the `user` table)**

| PK? | Column Name | Data Type | Description                                                                                         |
| --- | ----------- | --------- | --------------------------------------------------------------------------------------------------- |
| `*` | pid          | `int`     | Unique identifier (primary key) for each user, assigned by the university.                         |
|     | name        | `str`     | Name of the user.                                                                           |
|     | ...         | *various*     | *Many more specific user fields are hidden here.*                                       |
----

> **IMPORTANT!** Recall the role of the *primary key*. Primary keys serve as the *unique identifier* for an item / record / row in your SQL table. Each key is unique, and you can easily refer to rows by this unique identifier. In the table above, the `*` denotes that a field serves as the table's primary key column.

Now that you have refreshed your memory on primary keys, let's get introduced to the *foreign key*.

### Foreign Keys

A ***foreign key*** in a database is a field that refers to the primary key *of another table*, allowing you to reference records in a different table based on their unique ID. Foreign keys enable us to establish a link between two tables based on the values in these fields.

For example, let's say that we wanted to add a field in our `organization` table that holds the *PID of the organization's President*. This would essentially link the `organization` and `user` tables and allow us to easily find the President of an organization by looking up this stored PID in the `user` table. We can add to the `OrganizationEntity` like so:

**`OrganizationEntity` Fields (columns in the `organization` table)**

| Key? | Column Name | Data Type | Description                                                                                         |
| --- | ----------- | --------- | --------------------------------------------------------------------------------------------------- |
| `*`  | id          | `int`     | Unique identifier (primary key) for each organization.                                              |
|     | name        | `str`     | Name of the organization.                                                                           |
|     | ...         | *various*     | *Many more specific organization fields are hidden here.*                                       |
| `<-` | president_pid  | *int*     | The PID of this organization's President.                                       |

> **NOTE:** Like how we used `*` to denote a **primary key** in a table, we will use `<-` to denote a **foreign key**.

Foreign keys are the **building block** for database relationships and tell SQL that a relationship exists between two tables.

How would we add this field to our `OrganizationEntity`?

### Modifying the Entity

We would imagine what our entity looks like before we attempt to add any relationships:

---
**In `entities/organization_entity.py`**

```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
```
---

So far, we have used the `mapped_column()` object to define fields in our table. How do we generate columns that contain *foreign keys?*

We can pass a `ForeignKey()` object into our column! Look at the following field to store the President's PID:

```py
# Establishes a one-to-one relationship between the organization and user tables.
president_pid: Mapped[int] = mapped_column(ForeignKey("user.pid"))
```

The parameter for the `ForeignKey()` object follows the format `table.field`. So in this case, since this column is a foreign key for the `pid` column of the `user` table, we pass `"user.pid"` as the parameter.

This is all we need to establish a relationship!

However, this is not all. How would be actually *access* the President `UserEntity` object for a given organization? Would we need to make another read in the database?

No! SQLAlchemy can actually take care of this in something called **relationship fields**. These are fields in the Entity that *DO NOT EXIST IN THE TABLE AS COLUMNS*, however its values are automatically populated by SQLAlchemy when reading data. This allows our entities to be populated with data from relationships.

We can use the `relationship()` object to define relationship fields! Take the example below for storing the user data of an organization's President:

```py
# Relationship Fields

# Stores the user data of the President, populated automatically by SQLAlchemy
# using the foreign key column we defined above.
president: Mapped["UserEntity"] = relationship(back_populates="president_for")
```

SQLAlchemy is smart enough to know to populate `president` with the `UserEntity` object with the *same PID* as the the value stored in the `president_pid` field.

We can also implement a relationship field in the `UserEntity` as well! We can do this to store which organization a user is president for. This can be done with the following:

```py
# Relationship Fields

# Stores the user data of the Organization this user is President for, populated
# automatically by SQLAlchemy using the foreign key column we defined above.
president_for: Mapped["OrganizationEntity"] = relationship(back_populates="president")
```

You may also notice the `back_populates="president_for"` and `back_populates="president"` as the respective parameters for both `relationship` objects. This is extremely important! Since there is a relationship between the `president` and `president_for` fields, the `back_populates` field *points to the relationship field in the other table*. This aids SQLAlchemy in filling in the correct values for these fields.

In total, here are both completed entities:

---
**In `entities/organization_entity.py`**

```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Establishes a one-to-one relationship between the organization and user tables.
    president_pid: Mapped[int] = mapped_column(ForeignKey("user.pid"))

    # Relationship Fields
    
    # Stores the user data of the President, populated automatically by SQLAlchemy
    # using the foreign key column we defined above.
    president: Mapped["UserEntity"] = relationship(back_populates="president_for")
```
---
**In `entities/user_entity.py`**

```py
class UserEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `User` table"""

    # Name for the users table in the PostgreSQL database
    __tablename__ = "user"

    # Fields
    pid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    # Relationship Fields
    
    # Stores the user data of the Organization this user is President for, populated
    # automatically by SQLAlchemy using the foreign key column we defined above.
    president_for: Mapped["OrganizationEntity"] = relationship(back_populates="president")
```
---

We can model the final relationship we established in the following diagram:
 
![One-to-One Diagram](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/relationships/docs/images/sqlalchemy/one-to-one.png)

This is extremely powerful! Take the original ticket from the introduction.  The ticket asked you to keep track of each organization's President in your database, eventually to be used to display the name of organizations' Presidents on each organization detail page. Now, with our new arrangement, we can easily access this data with `organization_entity.president.name`.

## Implementing a One-to-Many Relationship

### Background

Setting up a one-to-many relationship in our entities is nearly identical to setting up one-to-one relationships with one change. Instead of one of our relationship fields holding just one value, we want it to store a list of values.

Let's take the following example. In the CSXL database, we have the `organization` table which stores information on organizations, and the `event` table that stores the events hosted in the CS community. We want to establish a relationship in our database such that we can relate events to the organizations that host them. We can easily determine that this relationship will be a *one-to-many* relationship because each organization can host numerous events, but each event is hosted primarily by one organization.

### Modifying the Entity

We can model this relationship in our entities like so:

---
**In `entities/event_entity.py`**
```py
class EventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Event` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "event"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Establishes a one-to-one relationship between the event and user tables.
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    # Relationship Fields
    
    # Stores the hosting organization, populated automatically by SQLAlchemy
    # using the foreign key column we defined above.
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")
```
---
**In `entities/organization_entity.py`**
```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    # Relationship Fields
    
    # Stores the events this org hosts, populated automatically by SQLAlchemy
    # using the foreign key column we defined above.
    events: Mapped[list["EventEntity"]] = relationship(back_populates="organization")
```
---

Notice that the *only difference* is that the `OrganizationEntity` stores a ***LIST*** of `EventEntity` objects because there are numerous events for one organization!

*In a one-to-many relationship, **we put the foreign key in the entity on the "many" side of the one-to-many relationship. Since there are many entities for one organization, we put the ID on the many side.*** We cannot put a foreign key column in `OrganizationEntity` because we would then need to store a list of IDs, which we cannot to in PostgreSQL.

We can model this using the diagram below:

![One-to-many relationship diagram](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/relationships/docs/images/sqlalchemy/one-to-many.png)

## Implementing a Many-to-Many Relationship

### Background

The last type of relationship that we can establish is the many-to-many relationship. This type of relationship is more involved to set up than the other two types of relationships. 

The main reason has to do with the fact that, in the previous types of relationships, we create a *foreign key* field in one of the entities that maps directly to a record in a different table! Also recall that we put this foreign key field in the entity on the "many" side of the one-to-one or one-to-many relationship, since then we only need to refer to one other item. This is important because in PostgreSQL, we cannot store a list of foreign keys as a field - only a single item.

The problem is, in a many-to-many relationship, *both sides* refer to many items - meaning that there is no adequate place to put the foreign key field. Because of this, we cannot directly establish a many-to-many relationship between two entities on their own.

Instead, we need a method by which we can *match together* the IDs from the left table and the IDs from the right table. We can do this by creating an **association table**.

### Association Tables

An **association table** is a table that matches together the IDs from two different tables, serving as a bridge to connect items from one table to items in another. Each record in an *association table* is defines an explicit relationship between two records.

Take a look at the diagram below:

![Association table diagram](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/sqlalchemy/docs/images/sqlalchemy/association.png)

In the diagram above, you can see that the association table matches together items from the *left* table and items from the *right* table. Ultimately, this establishes a many-to-many relationship because, for example, `LeftEntity(id=1)` maps to two items in the `right` table, one of which being `RightEntity(id=2)`; meanwhile, `RightEntity(id=2)` maps to two items in the `left` table, one of which being `LeftEntity(id=1)`.

Also notice that the ***association table** is where our foreign key columns are now placed!** So, we establish a relationship between the tables in our PostgreSQL database.

Remember that entities define tables in our database. So, in order to actually create an association table though, **we must add another entity**.

### Creating the Association Table Entity

For the sake of example, say we are trying to implement the *event registration feature*, which will establish a many-to-many relationship between the `event` table and the `user` table. We know this is a many-to-many relationship because each event can have many registered users, and users can also register for many events at once. 

So, in order to establish a many-to-many relationship between these two tables, we must create a new *association table*. Let's call this `event-registrations` and the entity `EventRegistrationEntity`. We can create this entity below:

---
**New File `entities/event_registration_entity.py`**
```py
class EventRegistrationEntity(EntityBase):
    """Serves as the association table between the event and user table."""

    # Name for the event registrations table in the PostgreSQL database
    __tablename__ = "event-registration"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Two foreign key fields, as shown in the table above, to connect the
    # event and user tables together.
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    user_pid: Mapped[int] = mapped_column(ForeignKey("user.pid"), primary_key=True)

    # TODO: Relationship Fields

```
---

You can see that this entity has *two foreign key fields* one to the `event` table and one to the `user` table! Now, these tables are connected. The only thing left to do is to add the relationship fields. We also make these our primary key fields too, since these two fields together uniquely identify each registration.

In this case, we could see the creation of the following relationship fields:

---
**In File `entities/event_registration_entity.py`**
```py
class EventRegistrationEntity(EntityBase):
    ...
    # Relationship Fields
    event: Mapped["EventEntity"] = relationship(back_populates="registrations")
    user: Mapped["UserEntity"] = relationship(back_populates="registrations")
```
**In File `entities/event_entity.py`**
```py
class EventEntity(EntityBase):
    ...
    # Relationship Fields
    registrations: Mapped[list["EventRegistrationEntity"]] = relationship(back_populates="event", cascade="all,delete")
```
**In File `entities/user_entity.py`**
```py
class UserEntity(EntityBase):
    ...
    # Relationship Fields
    registrations: Mapped[list["EventRegistrationEntity"]] = relationship(back_populates="user", cascade="all,delete")
```
---

> **NOTE:** Notice the addition of `cascase="all,delete"! This means that when you delete an event or a user, all of the associated registrations to it are also deleted. This prevents fractured relationships when entities are deleted. If you are testing your code and deleting an entity in a many-to-many relationship is not working, double-check that you have a `cascade` rule set up!

This is great! We now have indirectly connected all of the events and users together via lists of `EventRegistrationEntity` objects. Let's take a look at this relationship in a simplified diagram:

![many-to-many-one](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/relationships/docs/images/sqlalchemy/many_one.png)

As you can see in the diagram, we have set up a many-to-many relationship by essentially setting up two one-to-many relationships between the `event` and `user` tables with the `event-registration` table. This adequately connects our data. For example, if you wanted to access all of the registered users for an event, you could run the following pseudocode:

```py
# Traditional list and loop
registered_users = []
for registration in event_entity.registrations:
    registered_users.append(registration.user)

# Or, more concisely in Python:
registered_users = [registration.user for registration in event_entity.registrations]
```

This is great, however this is not a *full* many-to-many relationship. Wouldn't it be great to store a list of `UserEntity` objects in the `EventEntity` and a list of `EventEntity` objects in the `UserEntity` directly?

We actually can also do this using relationship fields! 

Look at the following code:

---
**In File `entities/event_registration_entity.py`**
```py
class EventRegistrationEntity(EntityBase):
    ...
    # Relationship Fields
    event: Mapped["EventEntity"] = relationship(back_populates="registrations")
    user: Mapped["UserEntity"] = relationship(back_populates="registrations")
```
**In File `entities/event_entity.py`**
```py
class EventEntity(EntityBase):
    ...
    # Relationship Fields
    registrations: Mapped[list["EventRegistrationEntity"]] = relationship(back_populates="event", cascade="all,delete")
    users: Mapped[list["UserEntity"]] = relationship(secondary="event-registration", back_populates="events")
```
**In File `entities/user_entity.py`**
```py
class UserEntity(EntityBase):
    ...
    # Relationship Fields
    registrations: Mapped[list["EventRegistrationEntity"]] = relationship(back_populates="event", cascade="all,delete")
    events: Mapped[list["EventEntity"]] = relationship(secondary="event-registration", back_populates="users")
```
---

We add two new fields: `users` in the `EventEntity` which stores a list of registered users, and `events` in `UserEntity` which stores a list of events the user is registered for. Notice the use of `secondary="event-registration"`! This parameter takes in the *name of an association table*, and SQLAlchemy does the rest - intelligently populating both lists (matching the fields together with their `back_populates` being set to each other). We can take a look at the new diagram:

![many-to-many-two](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/relationships/docs/images/sqlalchemy/many_two.png)

Now, if you wanted to see the registered users for an event, it is easier than ever:
```py
registered_users = event_entity.users
```

This is the ideal way that most many-to-many relationships are constructed, and the convention you should use in your final projects!

## Updating the Models

### Background

Great! Now that you have updated your entities to support relationships, we must now update our models to reflect our changes.

Let's use the *one-to-many* organization to events relationship we completed in a previous section. Recall the finalized entities:

---
**In `entities/event_entity.py`**
```py
class EventEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Event` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "event"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Establishes a one-to-one relationship between the event and user tables.
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    # Relationship Fields
    
    # Stores the hosting organization, populated automatically by SQLAlchemy
    # using the foreign key column we defined above.
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="events")
```
---
**In `entities/organization_entity.py`**
```py
class OrganizationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "organization"

    # Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    # Relationship Fields
    
    # Stores the events this org hosts, populated automatically by SQLAlchemy
    # using the foreign key column we defined above.
    events: Mapped[list["EventEntity"]] = relationship(back_populates="organization")
```
---

We should then be able to update our models:

---
**In `models/event.py`**
```py
from pydantic import BaseModel
from .organization import Organization

class Event(BaseModel):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int | None = None
    name: str
    organization_id: int
    organization: Organization
```
---
**In `models/organization.py`**
```py
from pydantic import BaseModel
from .event import Event

class Organization(BaseModel):
    """
    Pydantic model to represent an `Organization`.

    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database.
    """

    id: int | None = None
    name: str
    events: list[Event]
```
---

Yay 🥳! That was easy, let's run our proj--

```
ImportError: cannot import name 'Event' from partially initialized module 'backend.models.event' (most likely due to a circular import)
```

NOOOoooo...

Receiving this error is heartbreaking, however it is quite a common problem - especially based on the way we have set up our models.

Understanding why this error occurs relies on having an understanding of *how* Python interprets code files. Every time Python reaches an import statement, it *reads through that file to its entirety*. So, given our model files, this is the result:

![circularity](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/sqlalchemy/docs/images/sqlalchemy/circularity.png)

Uh oh.. We ran into an infinite loop. Very sad.

### Resolving Model Circularity

We can come up with a clever way to solve this problem - *separating our fields from our entity relationship fields into a separate model*. In this project, we call these **Detail models**.

Look at the following setup:

---
**In `models/event.py`**
```py
from pydantic import BaseModel

class Event(BaseModel):
    """
    Pydantic model to represent an `Event`.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database
    """

    id: int | None = None
    name: str
    organization_id: int
```
---
**In `models/event_details.py`**
```py
from .organization import Organization

class EventDetails(Event):
    """
    Pydantic model to represent an `Event`, including back-populated
    relationship fields.

    This model is based on the `EventEntity` model, which defines the shape
    of the `Event` database in the PostgreSQL database.
    """
    organization: Organization
```
---
**In `models/organization.py`**
```py
from pydantic import BaseModel

class Organization(BaseModel):
    """
    Pydantic model to represent an `Organization`.

    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database.
    """

    id: int | None = None
    name: str
```
---
**In `models/organization_details.py`**
```py
from .event import Event

class OrganizationDetails(Organization):
    """
    Pydantic model to represent an `Organization`, including back-populated
    relationship fields.

    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database.
    """

    events: list[Event]
```
---

Notice that all of our detail fields ***inherit their other properties*** from the main non-detail model! This means that detail models are essentially extensions that contain the relationship fields.

Now, let's look at how Python follows this code:

![no circularity](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/sqlalchemy/docs/images/sqlalchemy/no_circularity.png)

As you can see, there is no longer circularity! There is a clear linear path from start to end.

Of course, adding details models does add a bit of complexity to your code, as you have to deal with two different models for the same data. However, this is the best way to prevent major migraine-inducing circularity issues throughout your codebase.

## Conclusion

I hope that this reading helps you gain an understanding of modeling relationships between your database tables for your final projects! Here are some further readings that may be of help:

- [Official SQLAlchemy Documentation on Relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#declarative-vs-imperative-forms)

