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

We would imagine what our entity looks like before we attempt to add and relationships:

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

## One-to-One Relationship

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

## One-to-Many Relationship

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

## Many-to-Many Relationship

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

## Modeling Relationships in the Entity

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
| --- | ----------- | --------- | ----------------------------------------------- |
| \*  | id          | `int`     | Unique identifier (primary key) for each event. |
|     | name        | `str`     | Name of the event.                              |
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

Modeling one-to-one or one-to-many relationships is easy, because in one table, we can store the primary key of the an entry in the other table to establish the relationship. However, how do we store _many_ primary keys in both tables? We are unable to use lists as data types in our PostgreSQL fields (as in it is bad practice). So, how can we match up numerous entries of two different tables together?

**Enter the join table.**

A **join table** is an intermediate table between the two tables in a many-to-many relationship whose sole purpose is to model the connection between both tables. Let's use _organization membership_ as an example.

Say that we want to establish a many-to-many relationship between the `organization` and `user` tables. We can connect these two tables in a many-to-many relationship by creating a central _join table_ - let's call it our `membership` table. Look at the following diagram below:

![Join table example diagram]()

All join tables are required to have three fields - one primary key to identify each membership, and then two fields for the primary key of each item that we are relating - in this case, this would be `org_id` and `user_pid`.

As you can see, each listing bundles together the ID of the organization and the PID of the user together to establish a relationship between two items. Since this join table can have many rows and values can repeat in each column, we can therefore have many users related to a single organization, and many organizations related to a single user - hence a _many-to-many relationship!_

Creating a join table in SQLAlchemy is pretty simple. Let's do this in a new file in the `/entity` backend directory. We can use the following convention in Python to do so:

```py
# Define the membership table to be used as a join table to persist
# a many-to-many relationship between the organization and user table.
membership_table = Table(
    "membership",
    EntityBase.metadata,
    Column("org_id", ForeignKey("organization.id"), primary_key=True),
    Column("user_pid", ForeignKey("user.pid"), primary_key=True),
)
```

You can see that the code to create join tables is a bit different than we had before with creating entities. The join table is a means to an end, and we will not be directly querying data from this membership table.

Now that we have created our intermediate

## Resolving Model Circularity
