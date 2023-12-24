# Academics Feature Technical Specification

> Written by [Ajay Gandecha](https://github.com/ajaygandecha) for the CSXL Web Application.<br> _Last Updated: 12/24/2023_

This document contains the technical specifications for the Academics feature of the CSXL web application. This feature adds _5_ new database tables, _25_ new API routes, and _12_ new frontend components to the application.

The Academics Feature adds UNC course data to the CSXL web application. The web application can now store data on UNC courses, course offerings / sections for each courses, and terms. Section data also stores instructors and TAs for a course, as well as lecture and office hour rooms.

All visitors to the CSXL page are able to view a _COMP Course Catalog_ to see all of the courses that the UNC Computer Sciende department offers, as well as a _Section Offerings_ page where students can view course sections being offered for various terms. Course data is modifiable to the CSXL web page administrator.

## Frontend Features

The admin features add _12_ new Angular components, all at the `/academics` route.

### User Features

The following pages have been added and are available for all users of the CSXL site. These pages are ultimately powered by new Angular service functions connected to new backend APIs.

#### Academics Home

![Academics home page](../images/specs/academics/academics-home.png)

The home page for the new Academics feature is available on the side navigation toolbar at `/academics`. The home page contains links to both the _course catalog_ and the _section offerings_ page.

In the future, this page will be heavily extended to add personalized academics features for users of the CSXL web app. For now, this page will remain static and exist merely for informational and navigational purposes.

This page is powered by new

#### Course Catalog

![Course catalog](../images/specs/academics/course-catalog.png)

The course catalog page serves as the main hub for students to learn more about COMP courses at UNC. The page exists at the `/academics/catalog` route. The course page shows the courses available in the backend. Right now, the course page shows this data in a simple table. Users can click on courses to see a dropdown to learn more about a course's _credit hours_ and _description_.

In the future, when more courses outside of just COMP courses are added here, this page will include a dropdown in the top right that allows users to switch the course subject they look for courses on.

#### Section Offerings

![Section offerings](../images/specs/academics/section-offerings.png)

The section offerings page serves as the main hub for students to view offerings of COMP courses by semester / term. The page exists at the `/academics/offerings` route. The section page shows this data in a table. Users can click on courses to see a dropdown to learn more about a course. There is also a dropdown in the top right that allows users to view course offerings based on all of the semesters / terms saved in the database.

In the future, when more courses outside of just COMP courses are added here, this page will include another dropdown in the top right that allows users to switch the course subject they look for courses on.
