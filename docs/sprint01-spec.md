# Technical Specification Documentation

David Foss, Ella Gonzales, Tobenna Okoli, Francine Wei

## New/Modified Model Representations and API Route
For this sprint we had to create an new API route for the PUT operation to edit open hours.

We did create the NewOperatingHours and NewOperatingHoursJSON models to facilitate the creation of new operating hours, as well as the parseOperatingHoursJSONArray method to facilitate getting operating hours from the backend.

## Database/Entity-Level Representation Decisions

While we interacted with the operating hours, we decided not to make any changes as our current feature set for this sprint did not require them.

## Technical Design Choices

**Calendar View:** We chose to implement a calendar widget rather than use an existing MaterialUI form as a time picker because we wanted to innovate on what currently exists on the CSXL website and create a potentially mergeable final project that will make the open hours editing process easier and more user friendly.

## User Experience Design Choices

**Calendar Time Ranges:** We chose to only show times between 8am and 10 pm over a 24 hour calendar, because currently the open hours of the CSXL fall within those times. We also chose to only show Monday through Friday for the same reason. In the event that an operating hours block is scheduled during a time that would normally not be shown, the calendar is automatically adjusted to allow the user to see it.

**Calendar View:** We chose to allow admins to add/edit the open hours on a calendar rather than a form because having the visual representation would make it easier to schedule and coordinate hours and dates.

**Sidebar Editing:** We considered using a dialog box for adding operating hours for mobile support concerns, however we decided to instead orient it as a sidebar to allow administrators to see the current schedule as they're adding new hours.

## Development Concerns

**frontend/src/app/coworking/coworking-home/coworking-home.component.ts:** First, the gear button that accesses and links an authorized user to the Open Hours Calendar Editor is located in this file. This gear button dictates the path to the new page that holds the operating hours calendar editor that an admin user can access.

**frontend/src/app/coworking/coworking-admin folder:** This folder was created to contain the landing page for the calendar. It contains the coworking-admin.component.ts file, coworking-admin.component.html file, and the coworking-admin.component.css file.

**frontend/src/app/coworking/coworking-admin/coworking-admin.component.ts:** This page contains the route used by the gear button to access the page. It also specifies the html template and css styling used for the page.

**frontend/src/app/coworking/coworking-admin/coworking-admin.component.html:** The html template contains the operating hours calendar widget and can be edited in the future to include any other components needed on the page.

**frontend/src/app/coworking/coworking-admin/coworking-admin.component.css:** The CSS file contains any classes and stylings used uniquely for the page.

**frontend/src/app/coworking/coworking-admin/coworking-operating-hours folder:** This folder was created to contain the component that allows an administrator to create/edit an operating hours entity.

**frontend/src/app/shared/operating-hours-calendar folder:** This folder contains the ts, html, and css files used to make the operating hours calendar and it’s functionalities.
While most of the styling for this section is defined in the css, there is a small portion defined in the html directly as it is dynamically generated, namely the grid layout of the calendar.
