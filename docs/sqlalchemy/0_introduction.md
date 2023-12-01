# SQLAlchemy Tutorial

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.
> _Last Updated: 11/16/2023_

## Preface

Throughout this course so far, you have been learning about each layer of the tech stack. You started in the frontend, with _Angular components_ - what the users see on each page. You then moved downwards to the _Angular services_, which help to fetch and update data for your application. You then began to explore the backend layer, using _FastAPI_ to expose data across HTTP to your frontend services. Lastly, you made it to the _backend service_ layer, which your APIs called to in order to manipulate data. These layers can be represented using this flowchart:

![Flowchart 1 showing everything except the ORM session and PostGres](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/images/sqlalchemy/tech-stack-no-db.png)

All of the layers you have been exposed to so far have enabled you to create extremely powerful web applications. However, there is one problem.

**_Your data does not save._**

You probably encountered this issue already. You refresh your page or restart your project, and all of the data that you worked with disappeared. In the real world, this is not the case. How many times have you gone onto Instagram and seen all of your photos disappear?

_This indicates that something is missing in our stack._

We are missing a place to _store data_ such that it **persists** - or, is _saved_ forever. We need a durable container that stores our data such that whether we refresh the page, restart our project, or update our live deployment (on CloudApps), our data remains in tact.

**Enter the database!**

The database is the core component of the _final layer of our COMP 423 tech stack_ - the **persistent data store**. The database is the durable container mentioned earlier that will keep our data in tact.

There are many different kinds of databases that we can use, however in COMP 423 and in the CSXL Web Application, we use a **PostgreSQL** relational database to store our data.

We can add this database component to our tech stack flowchart:

![Same flowchart as before but with PostgreSQL Database](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/images/sqlalchemy/tech-stack-db.png)

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

Of course, this is super cool! However, there are a few problems. It is quite hard to write and execute pure SQL queries in Python. Plus, there is a lot of things behind the scenes to manage here. We need a tool that allows us to connect to our SQL database from Python so that we can manage the data in our database.

**Enter SQLAlchemy!**

**SQLAlchemy** is the primary SQL toolkit that we will use to interact with our PostgreSQL database. An active SQLAlchemy _session_ serves as the bridge between the existing Python backend services and the data in your PostgreSQL database, allowing you to perform **CRUD operations** _(create, read, update, delete)_.

Take a look at how the SQLAlchemy session sits in with our stack diagram:

![Same flowchart as before but with SQLAlchemy](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/images/sqlalchemy/tech-stack-with-alchemy.png)

Now, the database is connected to the rest of the application!

## Motivations

There are many reasons why you would want to use SQLAlchemy rather than just writing and running SQL queries manually.

- First, SQL queries would just be written as strings in Python. Manually building up these strings with concatenation is _messy and error-prone_. SQLAlchemy allows us to interact with our database by handling this SQL query creation for us, and we just have to call certain methods to perform the actions we want.

- In addition, when it comes to actually _running_ string SQL queries on the database is difficult and would require us to write a lot of extra service code anyway.

- There are also _security risks_ with allowing pure SQL strings to be used on the database. Malicious SQL queries would easily be run on the database, causing major issues. SQLAlchemy mitigates these attacks and handles which data should be acessible or not.

- As you will learn in future chapters, SQLAlchemy also handles the conversion between SQL data and Python objects, allowing you to easily with with data you retrieve from the database and write data from Python.

- Different types of SQL databases (Postgres, MySQL, SQLite, etc) all are slightly different - either in features, data types they support, and so on. SQLAlchemy takes care of this for us so that we can just interact with our database like we would expect.

This series of tutorials is dedicated to helping you become familiarized with SQLAlchemy and how it is used in the CSXL Application.

## Table of Contents

[**Chapter 1: SQLAlchemy Core and ORM**](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/sqlalchemy/1_sqlalchemy_core_and_orm.md)

This chapter introduces the SQLAlchemy Core and ORM and breifly explains the function of each in the context of the database and overall backend.

[**Chapter 2: SQLAlchemy Entities**](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/sqlalchemy/2_entities.md)

This chapter introduces SQLAlchemy Entities to model database tables in Python, how to set them up, and how they differ from the Pydantic models you are already using in your backend.

[**Chapter 3: Connecting to the Database**](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/sqlalchemy/3_connecting_to_database.md)

This chapter introduces how you programmatically create the SQLAlchemy session to interact with your database, show how this is managed, and describe how the session is injected into backend services.

[**Chapter 4: CRUD Operations**](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/sqlalchemy/4_crud_operations.md)

This chapter discusses how you can use SQLAlchemy to interact with your database, including how to run common operations such as creating, reading, updating, and deleting data. This chapter also includes supplemental resources for more complex SQLAlchemy queries.

[**Chapter 5: Database Relationships**](https://github.com/unc-csxl/csxl.unc.edu/blob/main/docs/sqlalchemy/5_relationships.md)

This chapter introduces the concept of database relationships. It introduces the motivation behind database relationships, discuss the different types, how to implement them using SQLAlchemy, and mentions common problems or pitfalls that you may face when adding relationships to your project.
