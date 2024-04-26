# TA Application Technical Specification

> Written by [Ben Goulet](https://github.com/bwgoulet) for the CSXL Web Application.<br> _Last Updated: 4/24/2024_

This document contains the technical specifications for the TA Application feature of the CSXL web application. This feature adds _2_ new database tables, _5_ new API routes, and _3_ new frontend components to the application.

The TA Application allows us to retrieve data on COMP UTA's via the CSXL web application. The web application can now store data on UNC COMP UTA's, with the eventual implementation of Graduate TA's on the horizon.

All logged-in users to the CSXL page are able to access the _Fall 2024 UTA Application_ to apply to be a UTA. UTA Applications will inevitably be unique per _term_, and are editable upon completion until the end of the application period. Application review is currently not implemented and performed directly via the PostgreSQL database.

## Table of Contents

- [Frontend Features](#FrontendFeatures)
  - [User Features](#UserFeatures)
    - [Academics Home](#AcademicsHome)
    - [UTA Application](#UTAApplication)
    - [Application Home](#ApplicationHome)
  - [Admin Features](#AdminFeatures)
  - [Conclusion](#Conclusion)
- [Backend Design and Implementation](#BackendDesignandImplementation)
  - [Entity Design](#EntityDesign)
  - [Inheritance Mapping](#InheritanceMapping)
  - [Pydantic Model Implementation](#PydanticModelImplementation)
  - [API Implementation](#APIImplementation)
  - [Permission Summary](#PermissionSummary)

## Frontend Features<a name='FrontendFeatures'></a>

The frontend features add _3_ new Angular components, with _2_ of them at the `/ta-application` route.

### User Features<a name='UserFeatures'></a>

The following pages have been added/updated and are available for all logged-in users of the CSXL site. These pages are ultimately powered by new Angular service functions connected to new backend APIs, just like all other features across the CSXL.

#### Academics Home<a name='AcademicsHome'></a>

![Academics home page](../images/specs/ta-application/academics-home.png)

The home page for the Academics feature now has a card for accessing the _Fall 2024 UTA Application_. When a user clicks 'Apply Now', the following notice pops up:

![Academics home page](../images/specs/ta-application/uta-notice.png)

From here, users can then click 'Apply' to be redirected to the application. Currently, the UTA Notice is its own component with hardcoded information. Ultimately, future developers may want to create a widget for TA Application notices - programatically filling in the HTML based on term data and application periods!

#### UTA Application<a name='UTAApplication'></a>

![UTA Application](../images/specs/ta-application/uta-application.png)

The UTA application page serves as the portal for the _Fall 2024 UTA Application_. This page contains the bulk of the new TA Application feature, which introduces new frontend elements to the CSXL.

#### Application Home<a name='ApplicationHome'></a>

![Application Home](../images/specs/ta-application/applications-home.png)

This is the landing page after completing the _Fall 2024 UTA Application_, and is the root route for 'ta-application'.

In the future, when more features related to applications are added, this page will become the home for all things "applications." Currently, this is not the case as admin features and the GTA Application are not implemented.

### Admin Features<a name='AdminFeatures'></a>

Admin Features are currently not available for the Fall 2024 application period. Come back here next semester!

### Conclusion<a name='Conclusion'></a>

In total, the following components have been added:

| Name                 | Route                             | Description                                                              |
| -------------------- | --------------------------------- | ------------------------------------------------------------------------ |
| **Application Home** | `/ta-application`                 | Main home page for the applications feature.                             |
| **UTA Application**  | `/ta-application/uta-application` | The UTA Application portal                                               |
| **UTA Notice**       | N/A                               | The pop-up before applying to be a UTA. Will eventually become a widget. |

## Backend Design and Implementation<a name='BackendDesignandImplementation'></a>

The TA Application feature ultimately adds _2_ new database tables and _5_ new API routes.

### Entity Design<a name='EntityDesign'></a>

The TA Application feature adds five new database tables and entities. They are as follows:

| Table Name            | Entity              | Description                                                           |
| --------------------- | ------------------- | --------------------------------------------------------------------- |
| `application`         | `ApplicationEntity` | Stores applications.                                                  |
| `section_application` | N/A                 | Stores sections, section preferences, and the associated application. |

The fields and relationships between these entities are shown below:

![Entity Design](../images/specs/ta-application/entity-relationships.png)

- <span style="color: black;">Black</span>: Current Design
- <span style="color: blue;">Blue</span>: to-Many relationship
- <span style="color: red;">Red</span>: to-One relationship
- <span style="color: green;">Green</span>: Not yet implemented

### Inheritance Mapping<a name='InheritanceMapping'></a>

The TA Application is the first feature of the CSXL to utilize a new technique for representing object-oriented hierarchies in our schema - inheritance mapping! This new technique allows us to create a schema that ultimately reflects the hierarchical nature of the TA Application. The inheritance tree for the TA Application is shown below:

![Inheritance Mapping](../images/specs/ta-application/application-inheritance.png)

Eventually, this will represent the full tree for the TA Applciation. Currently, `Application`, `UTA`, and `New_UTA` have been implemented for the _Fall 2024 UTA Application_. `Returning_UTA` is currently a part of the schema, but there is no use for the subclass this upcoming Fall. This subclass will eventually represent the many returning UTA's in the spring of '25. Finally, everything in green has not yet been implemented - but this half of the tree will represent all Graduate TA's.

As for the _type_ of inheritance mapping the TA Application employs, we're using a **single-table inheritance** structure. This just means that _all classes in a hierarchy are mapped to a single database table_ - `application`.

### Pydantic Model Implementation<a name='PydanticModelImplementation'></a>

### API Implementation<a name='APIImplementation'></a>

The TA Application feature adds 5 new API routes to handle CRUD operations on applications.

Here is a summary of the APIs added:

#### Applications APIs:

![Applications APIs](../images/specs/ta-application/api.png)

### Permission Summary<a name='PermissionSummary'></a>

All of these API routes call on **backend service functions** to perform these operations. These backend services are protected by permissions. Here is a summary of the permissions that this feature added:

| Action                  | Resource              | Description                                                       |
| ----------------------- | --------------------- | ----------------------------------------------------------------- |
| `"applications.create"` | `"applications/{id}"` | Gives the user permission to create applications in the database. |

<!-- ## Future Considerations<a name='FutureConsiderations'></a> -->
