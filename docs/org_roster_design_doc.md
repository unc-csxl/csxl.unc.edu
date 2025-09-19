# Student Organization Management Experience Thing (SOMEThing)
---
## Overview

Currently, organizations have no way to control their membership or interact with the CSXL in varying capacities based on their leadership privileges. It would be useful to perform actions like control the roster, create events, and reserve spaces that are tightly integrated with the CSXL website, but this would require that organizations store information about membership and leadership first.

---
## Key Personas

**Nolan No-Club:** Students who are not part of any organization. They are able to view every clubs’ leadership hierarchy and their recruitment processes.

**Pepper President:** Students who are in the highest level leadership position in a given organization. They should be able to customize the organization settings and have admin privileges to all main actions, such as creating events, managing the roster and more.

**Orestes Officer:** Students who are elevated above general membership and have certain privileges depending on their role. Every organization may control their hierarchy differently, so specific position privileges can be created customized by admins using checkboxes. 

**Alennikamy Admin:** Individuals who have administrative access to the CSXL website. They are able to delegate permissions of different organizations to students based on their roles and have the power to override or modify all settings and entities.

**Margarine Member:** Students who are members of one or more clubs. They should be able to see and/or participate in club events and news related to the clubs they are in.

---
## User Stories

**Nolan No-Club:** As a student who is not in an organization, I want to distinguish the availability of all the student organizations, so that I know how to join the ones I am interested in.

**Pepper President:** As a student who is an organization leader, I want to be able to accept prospective club members, customize organization settings, and create events and announcements so that I can have the highest privileges to manage my organization.

**Orestes Officer:** As a student who is on the executive team, I want to have access to role-specific privileges so that I can effectively help manage my organization.

**Alennikamy Admin:** As a CSXL website administrator, I want to give and restrict access according to the needs of each organization, so that I can effectively manage the organizations hosted by the site. 

**Margarine Member:** As a student who is a member of an organization, I want to be able to see my club’s information, so that I can stay up to date on important information that is relevant to my club.

---
## Figma: 

https://www.figma.com/design/AfYkqBBSxwhc10iTicUWOt/423-Sprint-00?node-id=11-1833&t=XfGCmMX9tCguB3wJ-1

---
## Wireframes and Mockups: 

**Organization Page:**
![Organization Page](https://github.com/user-attachments/assets/ba946081-455c-42c6-b4de-dfb9b95d7685)

**View Organization (General View):**
![View Organization (General Member)](https://github.com/user-attachments/assets/7e87e2ee-81e4-41ff-adce-9f834cb019d6)

**Edit Organization (Admin):**
![Officer)](https://github.com/user-attachments/assets/e2367763-18f9-4fc7-9de2-1be1362ce8d6)

**Edit Roster (Admin):**
![Component 2](https://github.com/user-attachments/assets/e8b743b0-7716-456a-8793-3b901963a96c)

---
## Technical Implementation Opportunities + Planning


### What specific areas of the existing code base will you directly depend upon, extend, or integrate with?

Organizations - search, details, join

### What planned page components and widgets do you anticipate needing in your feature’s frontend?

Buttons, Chips, Lists, Side bar panels, Tiles, Checkboxes

### What additional models, or changes to existing models, do you foresee needing (if any)?
<ol>
<li>Change to organization model to include leadership and roster and application type</li>
<li>Add leadership role model - with name, privileges, and current users</li>
<li>Add roster model - list of users</li>
</ol>

### Considering your most-frequently used and critical user stories, what API / Routes do you foresee modifying or needing to add?
<ol>
<li>roster - create it and setget info</li>
<li>organization - setget more info</li>
<li>leadership roles - setget more info</li>
<li>admin behind the scenes setget privileges</li>
</ol>

### What concerns exist for security and privacy of data? Should the capabilities you are implementing be specific to only certain users or roles? (For example: When Sally Student makes a reservation, only Sally Student or Amy Ambassador should be able to cancel the reservation. Another student, such as Sam Student, should not be able to cancel Sally’s reservation.)
<ol>
  <li>Roster should not be editable except for by admin or executive members</li>
  <li>Events should not be editable by lower roles</li>
  <li>Should not be able to see private student information unless they opt in somehow</li>
  <li>Club application state should be hidden except to approvers</li>
</ol>
