# SQLAlchemy Core and ORM

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.
> _Last Updated: 11/6/2023_

## Preface

SQLAlchemy is a Python library whose functionality is broken up into two parts - the **Core** and the **ORM**. In this chapter, you will be briefly introduced to both of these parts, their functionality, and how they work together to enable your web application to inteface with our SQL database.

## SQLAlchemy Core

The **SQLAlchemy Core** contains the base features for SQLAlchemy to serve as a _database toolkit_. First, the **Core** contains features features for SQLAlchemy to manage a constant connection with your database using the **SQLAlchemy Engine**. The _Engine_ uses important database information noted in your hidden `.env` secrets file to maintain a stable connection to the database. You will learn more about how to configure the engine and set up this connection to the database in [**Chapter 3: Connecting to the Database**](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/sqlalchemy/3_connecting_to_database.md).

The _Core_ also contains all of the logic needed to run SQL queries on the database and retrieve results. You have the _Core_ to thank for not having to write plain SQL code throughout your web application's backend!

## SQLAlchemy ORM

The **SQLAlchemy ORM (Object Relational Mapper)** extends the base functionality of the _Core_ to add _object relational mapping_ functionality. SQL tables have unique data types that are used to constrain and represent the values in each column. Essentially, the _object relational mapper_ is responsible for converting data from your SQL tables in SQL format to the format of a traditional Python object called an _entity_. You will learn about creating entities extensively in [**Chapter 2: SQLAlchemy Entities**](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/sqlalchemy/2_entities.md).

The _ORM_ enables you to easily transfer data between your SQL database and Python backend. The ORM also includes the _SQLAlchemy session_, the object which you will call to run SQL commands using _Python objects_ rather than pure SQL! You will also define the _session_ in [Chapter 3](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/sqlalchemy/3_connecting_to_database.md), however you will use the session extensively to interact with the data in your database in [**Chapter 4: CRUD Operations**](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/sqlalchemy/4_crud_operations.md).

## Final Thoughts

For the purposes of this project and COMP 423, the inner workings of the **Core** and the **ORM** are generally not within your concern. Howevever, you will be using both features from the _Core_ and the _ORM_ **_extensively_** to power the entire backend of your application - therefore, it is important to be aware of their existence and their functionality.

## Further Reading

- [Official SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/intro.html) about the Core and ORM
- [SQLAlchemy Core-Specific Documentation](https://docs.sqlalchemy.org/en/20/core/index.html)
- [SQLAlchemy ORM-Specific Documentation](https://docs.sqlalchemy.org/en/20/orm/index.html)
