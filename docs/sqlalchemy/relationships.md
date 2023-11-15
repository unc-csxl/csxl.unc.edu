# Database Relationships

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

As you can see based on the descriptions of the different types of relationships, our User and President example is best realized using a one-to-one relationship. It is extremely important to carefully think through the feature you are trying to add and which type of relationship you will need to successfully model your data. Depending on the relationship you want to establish, you will need to modify your SQLAlchemy entities differently.

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
 
![One-to-One Diagram]()

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

![One-to-many relationship diagram]()


## Many-to-Many Relationship

The last type of relationship that we have is a **many-to-many** relationship. In this type of relationship, an item in one table may be related to many items in the other table, and items in the other table can be related to many items in the original table!


## Resolving Model Circularity
