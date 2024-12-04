# Open Hours Editor Technical Specification

> [David Foss](https://github.com/fossinating), [Ella Gonzales](https://github.com/ellagonzales), [Tobenna Okoli](https://github.com/TJOKOLI17), [Francine Wei](https://github.com/francinew6)  
> [GitHub Repository](https://github.com/comp423-24f/csxl-team-a8)  
> _Last Updated: 12/04/2024_

This document outlines the technical specifications for the Open Hours Editor feature of the CSXL web application. This feature adds functionality to manage open hours directly through a user-friendly interface, improving administrative efficiency. The project introduces several new frontend components and utilizes existing API routes with minimal modifications to achieve its goals.

---

## Table of Contents

1. [Overview](#overview)
2. [New/Modified Model Representations and API Routes](#models-and-api)
3. [Database/Entity-Level Representation Decisions](#database-decisions)
4. [Technical Design Choices](#technical-design)
5. [User Experience Design Choices](#ux-design)
6. [Design Trade-Offs](#trade-offs)
7. [Development Concerns](#development-concerns)
8. [Screenshots and Descriptions](#screenshots)
9. [Future Considerations](#future-considerations)

---

## Overview<a name="overview"></a>

The Open Hours Editor provides a calendar-based interface for administrators to add, edit, and manage the open hours of the CSXL. This feature enhances usability by offering visual scheduling tools while maintaining consistency with existing site design.

---

## New/Modified Model Representations and API Routes<a name="models-and-api"></a>

- **API Route**:  
  A new `PUT` operation was added to edit open hours (`/api/openhours/edit`).

- **Models**:  
  Two new models were created:

  - `NewOperatingHours`: Represents a single set of operating hours.
  - `NewOperatingHoursJSON`: Handles JSON serialization for operating hours data.

- **Helper Methods**:
  - `parseOperatingHoursJSONArray`: Processes JSON data from the backend for frontend compatibility.

---

## Database/Entity-Level Representation Decisions<a name="database-decisions"></a>

While we interacted with the `OperatingHours` entity, no changes were made to the database schema. The existing entity provided sufficient functionality for this sprint.

---

## Technical Design Choices<a name="technical-design"></a>

1. **Custom Calendar Widget**:

   - We implemented a calendar widget to provide an intuitive, visual interface for managing open hours, rather than relying on a simpler time picker.

2. **Dynamic Calendar Adjustments**:

   - The calendar adjusts dynamically to display scheduled hours even if they fall outside the typical 8 AM–10 PM range.

3. **Highlighting Selected Hour Blocks**:
   - The selected hour block changes color during editing, providing clear visual feedback to the user.

---

## User Experience Design Choices<a name="ux-design"></a>

1. **Pop-Up Panels for Add/Edit Hours**:

   - The Add/Edit actions are handled through a pop-up panel, keeping the main calendar view uncluttered.

2. **Simplified Calendar View**:

   - The calendar only displays Monday through Friday and hours from 8 AM to 10 PM, reflecting current CSXL operating hours.

3. **Sidebar Editing**:
   - A sidebar was chosen for editing hours, allowing users to see the full calendar while managing operating hours.

---

## Design Trade-Offs<a name="trade-offs"></a>

### Technical Design Trade-Off: Sidebar vs. Persistent Panel

- **Decision**: We implemented a pop-up sidebar for editing instead of a persistent panel.
- **Reasoning**: The sidebar ensures the UI remains uncluttered, while allowing administrators to view the calendar as they manage open hours.
- **Trade-Off**: A persistent panel would have streamlined the workflow slightly but at the cost of reduced calendar visibility.

### User Experience Design Trade-Off: Add Hours Button vs. Direct Calendar Interaction

- **Decision**: We opted for an "Add Hours" button instead of direct calendar interaction for adding hours.
- **Reasoning**: The button simplifies interactions and prevents accidental scheduling errors.
- **Trade-Off**: While direct calendar interaction would be faster for experienced users, it could confuse new users and increase UI complexity.

---

## Development Concerns<a name="development-concerns"></a>

1. **Frontend Components**:

   - **`frontend/src/app/coworking/coworking-home/coworking-home.component.ts`**:  
     Contains the gear button that grants access to the Open Hours Calendar Editor.

   - **`frontend/src/app/coworking/coworking-admin folder`**:  
     Houses the main calendar component and related files, including:

     - `coworking-admin.component.ts` (logic and routing)
     - `coworking-admin.component.html` (template for the calendar view)
     - `coworking-admin.component.css` (styling for the calendar page).

   - **`frontend/src/app/shared/operating-hours-calendar folder`**:  
     Contains the reusable `OperatingHoursCalendar` component, which dynamically renders the calendar and applies styling.

2. **Dynamic Calendar Styling**:
   - The grid layout for the calendar is dynamically generated within the HTML and styled via CSS.

---

## Screenshots and Descriptions<a name="screenshots"></a>

### Default View

![Default View](https://github.com/comp423-24f/csxl-team-a8/blob/stage/docs/images/defaultView.png)  
**Description**: Displays the weekly open hours with buttons to add or edit hours.

### Add Hours Pop-Up

![Add Hours View](https://github.com/comp423-24f/csxl-team-a8/blob/stage/docs/images/addHoursView.png)  
**Description**: The "Add Hours" button triggers this panel for creating new open hours.

### Edit Hours Pop-Up

![Edit Hours View](https://github.com/comp423-24f/csxl-team-a8/blob/stage/docs/images/editHoursView.png)  
**Description**: Selecting an existing hour block highlights it and opens this panel for edits.

---

## Future Considerations<a name="future-considerations"></a>

1. **Direct Calendar Interaction**:

   - Enable users to click directly on a day to add hours, complementing the "Add Hours" button.

2. **Recurring Hours**:

   - Add a recurrence hour feature for streamlined scheduling.

3. **Mobile Optimization**:

   - Refactor components to improve mobile usability, including touch-friendly interactions.

4. **Expanded Time Range**:

   - Consider extending calendar hours and days for special events or unique schedules.

5. **Enhanced Styling**:
   - Incorporate additional visual cues and animations to improve accessibility and aesthetics.
