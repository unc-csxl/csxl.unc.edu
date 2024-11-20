# Open Hours Editor

David Foss, Ella Gonzales, Tobenna Okoli, Francine Wei

## Overview

Currently, there is no way within the UI to create new operating hours. By providing a way to add new operating hours from within the UI, this feature will improve usability for the administrators of the site. With this new functionality, staff can efficiently manage CSXL’s open hours, saving time and reducing errors in scheduling, ultimately improving the overall administrative efficiency.

## Key Personas

- **Adam Admin**: Needs an intuitive way to add, and update, and manage the open hours of the CSXL, including reflecting special events and breaks.
- **Sally Student**: Needs to be able to check the open hours of the CSXL to plan visits accordingly.

## User Stories

**Minimum Viable Feature Primary User Stories**

- As Adam Admin, I would like to be able to create new operating hours for the CSXL so that users can access our services.
- As Adam Admin, I would like to be able to delete operating hours in the future so that I can fix mistakes if I create incorrect operating hours.
- As Adam Admin, I would like to be able to see upcoming operating hours so that I can confirm they are properly configured.
- As Adam Admin, I would like to be able to edit upcoming operating hours so that I can fix errant configurations.
- As Sally Student, I would like to be able to see the operating hours so that I can know when I can use the CSXL.

## Wireframes/Mockups

**Default View**: When clicking the Coworking button, administrators are directed to a screen showing the weekly open hours, with options to add or edit hours as needed.
![Default View image](https://github.com/comp423-24f/csxl-team-a8/blob/stage/docs/images/defaultView.png)

**Add Hours View**: When the “Add Hours” button or a specific date on the calendar is clicked, a pop-up frame appears for creating new open hours.
![Add Hours View image](https://github.com/comp423-24f/csxl-team-a8/blob/stage/docs/images/addHoursView.png)

**Edit/Delete View**: Selecting an existing hour block highlights the block, and triggers an “Edit Open Hours” pop-up, allowing administrators to adjust or delete the selected open hours.
![Edit Hours View image](https://github.com/comp423-24f/csxl-team-a8/blob/stage/docs/images/editHoursView.png)

To get a closer look, view the Figma page: [Comp 423 Final Project Mock-Up](https://www.figma.com/design/W0XNaOzGnFZ3hPTxC5fmVV/Comp-423-Final-Project-Mock-Up?node-id=11-1833&t=Dqln3s7bTmiDOzPb-1)

## Technical Implementation Opportunities and Planning

1. Code Base Dependencies: We will depend directly on the existing API endpoints to create, edit, and remove operating hours. Specifically, this will involve extensions to the coworking page by adding a new button to allow administrators to edit the operating hours.
2. Frontend Widgets: We plan to develop a custom calendar widget, along with using the existing datetime selector from the office hours editor, and standard button components for a consistent interface.
3. Additional Models: No new models or changes to existing models are anticipated for this feature.
4. API Routes: We don’t foresee needing to modify or add any API routes.
5. Security and Privacy: Access to modifying open hours should remain restricted to authorized administrators. While API routes are already protected, the UI will also ensure non-admin users don’t see these options, minimizing potential confusion.
