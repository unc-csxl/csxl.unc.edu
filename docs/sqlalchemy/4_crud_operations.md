# CRUD Operations

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br>_Last Updated: 11/16/2023_

## Preface

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

## Transactions

In order for us to perform CRUD operations on our database, we must understand how these operations are performed. SQLAlchemy performs these operations using something called **_transactions_**. The purpose of a transaction is to denote an all-or-nothing collection of changes to a database. All-or-nothing refers to the fact that either _all_ of the requested changes should happen to the database. If something happens that would cause any change to fail, then _none_ of the changes are performed. This is incredibly vital for the integrity of the database. It ensures that the database is always in a consistent state even if errors occur, such as if a database modification fails, connection is dropped, in the middle of a transaction.

Consider the example used in class - transferring money between two bank accounts. Say that Kris Jordan bought his coworker, KMP, lunch. KMP wants to pay Kris Jordan back for $10. The following operations would be performed:

- `-$10` is removed from KMP's bank account
- `+$10` is added to Kris Jordan's bank account

In an ideal world, this transaction would occur and no issues would arise. But, what happened if, for example, there was a power outage in the middle of this transaction? One of four results could occur:

- KMP loses $10 and Kris Jordan gains $10, all is well.
- KMP loses $10 and Kris Jordan gains $0, meaning $10 disappeared!
- KMP loses $0 and Kris Jordan gains $10, meaning $10 spontaneouly appeared!
- Nothing happens.

For accounting purposes, the 2nd and 3rd scenarios are super bad. So instead, imagine that the two steps above (`-$10` and `+$10`) are *bundled into one transaction*.

Then, if the internet shuts off, the only two results could occur:

- KMP loses $10 and Kris Jordan gains $10, all is well.
- Nothing happens.

This eliminates the two worst outcomes! Either both statements are committed at the same time and the transaction succeeds, or neither is and the transaction gets "rolled back". When a rollback occurs, it's as if every statement earlier in the transaction is cancelled and never happened.

## Read Data

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
    .where(OrganizationEntity.public == true)
    .all()
```

We pass in `OrganizationEntity` into `.query()` like we did with `select()`, but now we need to add a filter! We add filters using the `.where()` method. This will append the filter condition to our query. We can filter our data for just when `OrganizationEntity.public == true`. Then, when we call `.all()`, the transaction runs and we get the data with the filter applied.

Our function might look something like:

```py
def all_public(self) -> list[Organization]:
    """Fetch all public organizations from the database"""
    entities = self._session.query(OrganizationEntity)
        .where(OrganizationEntity.public == true)
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

## Write Data

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

## Delete Data

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

## Supplemental: Advanced Querying Techniques

In the _Read Data_ section above, you learned about various methods for writing simple queries to retrieve data from your database. This supplemental section will add more advanced querying techniques to your toolkit to write more thoughtful and powerful queries.

### Boolean Logic (`AND` and `OR`) in Queries

We can implement boolean logic into our queries - specifically, the `AND` and `OR` operations. This allows us to create more complex queries and can help support numerous functions within your project.

#### Creating an `AND` Query

There are two methods by which we can create an AND query. By default, adding multiple `.where()` calls to a single query automatically pairs together as an `AND` call. For example, take the following code snippet:

```py
entities = self._session.query(OrganizationEntity)
    .where(OrganizationEntity.public == true)
    .where("Carolina" in OrganizationEntity.name)
    .all()
```

This will return all of the organizations that are *public* ***AND*** *have "Carolina" in their name!*

We can also create the *same query* using the logic below:

```py
entities = self._session.query(OrganizationEntity)
    .where(OrganizationEntity.public == true, "Carolina" in OrganizationEntity.name)
    .all()
```

The `.where()` method can actually take in multiple conditions, and the conditions that it accepts are all joined together using the boolean operator `AND`. So, this will *also* return all of the organizations that are *public* ***AND*** *have "Carolina" in their name!*

#### Creating an `OR` Query

Creating an `OR` query requires a little bit more, specifically, knowledge of Python's `|` operator. This operator will allow us to join two query conditionals together and apply the `OR` rule to it. For example,

```py
entities = self._session.query(OrganizationEntity)
    .where((OrganizationEntity.public == true) | ("Carolina" in OrganizationEntity.name))
    .all()
```

> **NOTE:** Both conditions are *surrounded by parenthesis*. You *MUST* do this when using the `|` operator or else unexpected results may occur!

This will return all of the organizations that are *public* ***OR*** *have "Carolina" in their name!*

There is also another shorthand method that allows you to build `OR` queries where you are trying to query based on alternative values for the same field. For example, take the following snippet:

```py
entities = self._session.query(OrganizationEntity)
    .where((OrganizationEntity.name == "CS+Social Good") | (OrganizationEntity.name == "AR+VR Club"))
    .all()
```

We can simplify this to:

```py
entities = self._session.query(OrganizationEntity)
    .where(UserEntity.name.in_(["CS+Social Good", "AR+VR Club"]))
    .all()
```

The `.in_()` method allows us to match a field based on alternative options! So, this code will return organizations with either the name `"CS+Social Good"` or `"AR+VR Club"`. 

> **NOTE:** The method has an underscore (`_`) in its name. This is because `in` is a reserved keyword in Python and therefore cannot be used anywhere else (such as method names). In fact, we used this keyword just a few examples ago in the conditional `("Carolina" in OrganizationEntity.name)`.

### Querying Based on Database Relationships

> **NOTE:** You will learn about database relationships in [Chapter 5](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/sqlalchemy/5_relationships.md) of this SQLAlchemy tutorial. If you have not reviewed Chapter 5 yet, check that out first!

Once your database tables grow in complexity, it is extremely likely that you will be trying to query data with relationships to other data - therefore, it is important to become familiar with how to query based on these relationships using SQLAlchemy.

#### Querying in a One-to-One or One-to-Many Relationship

Let's take the `organization` table that we have been examining throughout the previous parts. In the actual CSXL application, the `organization` table has a one-to-many relationship to the `event` table - because an organization can host many events, yet events can only be hosted by one organization.

What if we wanted to write a query to retreive all of the events for a specific organization?

```py
entities = self._session.query(EventEntity)
    .join(OrganizationEntity)
    .where(OrganizationEntity.shorthand == "CADS")
    .all()
```

First, we use query the `EventEntity` objects, because this is the format of the data that we are expecting. The next step here is to use the `.join()` method. The join method connects the `event` table, what we are querying on, to another table that is related to the `event` table. In this case, since the `event` table is related to the `organization` table, we can use `OrganizationEntity` inside of our `.join()` method.

*Now, we can filter our events based on the properties of the organizations they are related to!*

So, the code snippet above will *return all of the events whose related organization's slug is "CADS"*. Ultimately, this snippet returns all of the events hosted by CADS.

#### Querying in a Many-to-Many Relationship

What if we wanted to query based on a many-to-many relationship?

Let's take the `event` table and the `user` table. Events can have multiple registered users, and users can be registered for multiple events - therefore, this is a many-to-many relationship. To recap from Part 5 of the SQLAlchemy docs, we have to establish an *association table* to properly define a many-to-many relationship. In this example, we have the `EventRegistrationEntity` serving as the association table entity for the `EventEntity` and the `UserEntity`.

What if we wanted to write a query to retrieve all of the events registered by a single user?

```py
entities = self._session.query(EventEntity)
    .join(EventRegistrationEntity) # NEW
    .join(UserEntity)
    .where(UserEntity.id == "7308888888")
    .all()
```

Notice that again, we the entity that we put into our `query()` method was the `EventEntity` because this is the type of data that we are expecting. The only real difference here is that we have *one extra `.join()` method call*. Since the `event` and `user` tables are related through the `event_registration` table, in order to ultimately join the `event` table to the `user` table, we have to go through the *association table* (`event_registration`) first! Once we join with the association table, we can then join to the final table. From there, we can now apply a filter on the `user` table.

So, the code snippet above will *return all of the events whose attended by a user with the id `7308888888`.

### Querying Paginated Data

_Coming soon._
