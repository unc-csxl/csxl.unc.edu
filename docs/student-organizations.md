# CSXL Student Organizations and Events

> This project is being developed by *[Ajay Gandecha](https://github.com/ajaygandecha)*, *[Jade Keegan](https://github.com/jadekeegan)*, *[Brianna Ta](https://github.com/briannata)*, and *[Audrey Toney](https://github.com/atoneyd)* for the **[UNC Computer Science Experience Lab (CSXL)](https://csxl.unc.edu)** and as part of *[COMP 423: Foundations of Software Engineering](https://comp423-23s.github.io)* at UNC-Chapel Hill taught by *[Professor Kris Jordan](https://github.com/KrisJordan)*.


## Overview

The primary goal of the CSXL Student Organizations and Events feature is to allow UNC CS students to **explore all CS organizations on campus**, **view upcoming events** hosted by these organizations, **join organizations and events**, and **catalog events** attended in the past.

In addition, this feature should allow administrators of CS organizations to *edit their organization profile*, *add events their organization plans to host*, and *view members who sign up to attend*.

This feature would also **help to standarize the CS organization events system** so students, organization administrators, and CSXL administrators can *keep track of organization membership, event interest, and event attendance*.

## Implementation

### Database

The CSXL website stores data using a **PostgreSQL database**, using the *SQLAlchemy* Python package to interact with the SQL database. The website also uses the *FastAPI* package to expose backend functionality via API routes accessible by the Angular front-end.

In order to successfully implement the features listed above, we had to ensure that the database stores the following:
- Information on all UNC *organizations* and relevant data.
- Information on all *events* that the organizations above were hosting.
- Extra information on *users*, including organization membership and events users wish to attend.

To achieve these goals, we added the **`organization`** and **`event`** tables to the PostgreSQL database, as well as modified the existing **`user`** database.

The tables store the following information:

#### The `Organization` Table

| Field | Type | Description |
| ---- | ---- | ----- |
| `id` | `int?` | Unique ID of the organization.
| `name` | `str` | Name of the organization.
| `logo` | `str` | Link to the logo image of the organization.
| `short_description` | `str` | Short description of the organization.
| `long_description` | `str` | Longer description of the organization.
| `website` | `str` | Primary URL for the organization's website, if applicable.
| `email` | `str` | Primary email address for the organization, if applicable.
| `instagram` | `str` | Link to the organization's Instagram page, if applicable.
| `linked_in` | `str` | Link to the organization's LinkedIn page, if applicable.
| `youtube` | `str` | Link to the organization's YouTube page, if applicable.
| `heel_life` | `str` | Link to the organization's UNC HeelLife page, if applicable.

#### The `Event` Table

| Field | Type | Description |
| ---- | ---- | ----- |
| `id` | `int` | Unique ID of the event.
| `name` | `str` | Name of the event.
| `time` | `datetime` | Time of the event.
| `location` | `str` | Location of the event in string representation.
| `description` | `str` | Description of the event.
| `public` | `bool` | Boolean describing whether the event is open to the public, or if the event is closed to organization members only.
| `org_id` | `int` | ID of the hosting organization.

#### The `Registration` Table

| Field | Type | Description |
| ---- | ---- | ----- |
| `id` | `int` | Unique ID of the registration.
| `user_id` | `int` | ID of the user registering.
| `event_id` | `int` | ID of the event.
| `status` | `int` | Type of registration (0 = Registered, 1 = Registered + Attended).

#### The `OrgRole` Table

| Field | Type | Description |
| ---- | ---- | ----- |
| `id` | `int` | Unique ID of the org role relationship.
| `user_id` | `int` | User ID referencing the user.
| `org_id` | `int` | Organization ID referencing the organization.
| `membership_type` | `int` | Type of membership (0 = Member, 1 = Executive, 2 = Manager)

#### Relationships

The tables above are great to represent *organization* and *event* data by themselves - however in order to provide any functionality to the application (for example, allowing users to join organizations and attend events, as well as letting organizations create events), we need to establish **database relationships**.

When establishing relationships between database, extra *relationship fields* are added to each object of data from the database. These relationship fields are not fields in the PostgreSQL tables themselves - rather, they are extra fields defined on the data objects once pulled from the database. These relationship fields on a data object shows all other data objects connected to it. For example, the data entity from the `event` table will include extra *relationship fields* denoting *which organization is hosting the event*, as well as *all of the user attending the event*. This is because these *organizations* and *users* are other data objects that are *connected* / *related to* the event object.

Below is a summary of the relationships established, including between which tables, the relationship types, and their respective descriptions and purposes.

  | Left Table | Right Table | Type | Description |
| ---- | ---- | ---- | ---- |
  |`organization` | `event` | One-to-Many | This relationship enables the connection between CSXL events and hosting organizations. For every event there is a single host, but the hosting organization might be able to host multiple organizations. |
  |`user` | `event` | Many-to-Many | This relationship enables the connection between users and CSXL events. Users may attend many events, and events have many attendees, requiring a many-to-many relationship to be established. the `registrations` table serves as the *association* table between the `user` and `event` tables. |
  |`user` | `organization` | Many-to-Many | This relationship enables the connection between users and CS organizations. Users may join many organizations, and organizations have many members, requiring a many-to-many relationship to be established. These relationships also hold the membership type as a value. Some members may be admins of the organization, while others are just general members. The `org_role` table serves as the *association* table between the `user` and `organization` tables. |

These relationships now work great and are represented in all of the *data models* (models representing how we use database data within our app), and *data entities* (shape of the data retreived from the database directly).

Due to specific quirks with Python and the backend architecture, there were significant errors with relationhip fields when converting from *entities* to *models* and vice-versa.  When we convert one entity to a model, we also have to convert all of the encapsulated entities into models as well. For two models that are related, this causes `.to_model()` from one to call the other, which calls the original, leading to an infinite spiral down into the dark world of recursion.

The solution to this was to create new, unique models that contained *all of the same information **except** the relationship fields*. These are known as `Summary` models. Through converting the encapsulated entities into *summary* models rather than regular models, we stop the infinite chain of recursion. This solution makes the code less readable because now there are duplicate models that with only one difference in the fields. This however is the most optimal solution for our purposes.

### Design Choices

#### Organization List Page

> INSERT IMAGE HERE

The organization list page is easily accessible from the sidebar and shows users a list of all of the Computer Science organizations at UNC. Users are able to see important information about organizations at a glance, as well as access organizations' social media profiles to learn more about the organizations and get involved. If the user wishes to see more information and potentially join the organization, users can press the "Details" button.

This page also includes a smart seach bar that searches queries over variations of organization names, acronyms, descriptions, and other details based on user input. This would allow users to not only find organizations by name, but also to potentially explore organizations based on topics that interest them.

The organization list page is fully-responsive and in a grid page. We preferred the grid organization so that users can see a large amount of organization on the screen without wasting space, as well as providing each organization tile with just the right optimized amount of space.

#### Profile Page

> INSERT IMAGE HERE

The profile page serves as the central hub for users to access and modify their own user information, check their status on which organizations they are apart of, as well as review which events they have signed up for and attended.

The profile page displays all of this information is easy-to-digest tiles, providing important information on the top-left, organizations below that, and all user events on the right-hand side.

The events pane also includes drop-downs containing more information about events. We believed that this was the best design approach so that users are able to both see an uncluttered list of events as well as see more details about future or past events.

The profile page is also fully-responsive so that users are able to easily check their information on mobile devices without sacrifing ease-of-use.

## Development Concerns

### Project Organization

This project is organized into two main directories - the **Python backend** using *FastAPI* and *SQLAlchemy* in the `/backend` directory, and the **TypeScript frontend** using *Angular* in the `/frontend` directory.

####  Backend Directory (`/backend`)

Within the backend directory are four more subdirectories:
- `/api` - Contains all of the exposed *FastAPI* API routes.
- `/entities` - Contains all of the data entities which represent data directly coming from the database.
- `/models` - Contains all of the data models and data summary models which represent data as would be used within the backend and middleware. When data is retreived from the database, entities are converted into models. When data is added to the database, models are converted into entities.
- `/script` - Contains scripts on *creating*, *resetting*, and *deleting* the PostgreSQL database. *Use these at your own risk, as these would delete or modify existing data!*
- `/services` - Contains all of the *abstracted functionality of database interactions* used by the the API routes.
`/test` - Contains all of the *pytests* to ensure that the services are working locally.

The `database.py` file configures the database, and `main.py` configures and starts up the backend.

The `requirements.txt` file contains all of the Python dependencies needed for the backend to run correctly.

*To install all of the requirements of the backend, in terminal, first run `cd backend` followed by `pip install -r requirements.txt`.*

#### Frontend Directory (`/frontend`)

The frontend directory is structured in the same way as most Angular projects. 

The starting point for the entire application would be the homepage, defined in the `home.component` defined in `frontend/src/app/home`. The side navigation bar containing links to all other pages can be found in the `navigation.component`.

The starting point for this particular feature would be the *`organization`* component, found in `frontend/src/app/organizations`.

Front-end installation instructions can be found in the `/docs/get_started.md` file.

### Important Considerations

This project definitely has a lot of moving parts and therefore can be confusing to navigate for a new developer.

There are a few important things to consider:
- The frontend and backend of this project are **completely separate** with *different underlying technologies and languages.* The backend is in *Python* and the frontend is in *TypeScript*. This is one of the most important things to keep in mind. The only connection between the backend and the frontend are the API routes. Besides the API routes, the frontend knows nothing from the backend and vice-versa.
- The front-end follows the web Material design standards. Using Material components is generally preferred over custom components since they conform to the design standard by default.
- When troubleshooting issues on the backend, ensure that the database has been configured correctly, that your `.env` file is correct, and also that you restart the backend when major changes are made. All API routes are accessible and nicely summarized through the docs route - for example - `http://localhost/docs`! Use this to your advantage when testing API routes.

## Future Work

Our feature is making great progress by this sprint, however there are a few things we might like to add or improve:
- Allow admins of organizations to see the lists of members who starred their organization.
- Allow the admin of the entire CSXL site to see a list of all registered users.
- Improve the event creation process and add email reminders.
