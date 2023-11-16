# SQLAlchemy Tutorial

> Written by Ajay Gandecha for the CSXL Web Application and for COMP 423: Foundations of Software Engineering.<br> > _Last Updated: 11/14/2023_

## Preface

Throughout this course so far, you have been learning about each layer of the tech stack. You started in the frontend, with _Angular components_ - what the users see on each page. You then moved downwards to the _Angular services_, which help to fetch and update data for your application. You then began to explore the backend layer, using _FastAPI_ to expose data across HTTP to your frontend services. Lastly, you made it to the _backend service_ layer, which your APIs called to in order to manipulate data. These layers can be represented using this flowchart:

![Flowchart 1 showing everything except the ORM session and PostGres](https://github.com/unc-csxl/csxl.unc.edu/blob/docs/querying/docs/images/sqlalchemy/stack-no-db.png)

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
