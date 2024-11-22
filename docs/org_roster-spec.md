# Technical Specifications Document

This document list the relevant technical aspects of the organization roster management feature.

## New and Modified Models:

### [NEW] OrganizationMembership:

id: int membership primary key  
user: User useful for populating member’s data  
organization_id: int identifies organization  
organization_slug: str useful for queries filtering by organization slug  
organization_role: OrganizationRole (enum)

### [NEW] OrganizationRole: enum with {PRESIDENT, OFFICER, MEMBER, ADMIN}

### Sample data representation for Sally Student as a member of CADS:

```
{
id = 1,
user: Profile =
{
id: 3,
pid: 222222222,
onyen: "user",
...
}
organization_id = 1,
organization_slug = "cads"
organization_role = OrganizationRole.MEMBER
}
```

We opted to call it a “membership” because the membership encapsulates a student, and a specific role per org. It might have been confusing to call it a “member” because the “member” seems synonymous with the “student”, but they are not actually the same, the membership encapsulates the student that the membership applies to.

## New and Modified API routes:

### Frontend API:

**GET organizations/{slug}/roster** <- gets the roster, which is a list of memberships  
returns OrganizationMembership[]  
name: getOrganizationRoster(slug)

**DELETE organizations/{slug}/roster/{member_id}** <- deletes one membership from the roster list  
returns void  
name: deleteOrganizationMembership(member_id)

**POST organizations/{slug}/roster** <- adds membership  
returns OrganizationMembership  
addOrganizationMembership(slug, user_id)

### Backend API:

**GET /{slug}/roster** <- gets the roster, which is a list of members  
returns OrganizationMembership[]  
name: get_roster_by_slug

**DELETE/{slug}/roster/{member_id}** <- deletes one member from the roster list, doesnt return anything  
name: delete_member

**POST {slug}/roster** <- adds member  
returns OrganizationMembership  
name: add_member_to_organization

## New and modified database/entity-level representations

**[NEW] OrganizationMembershipEntity (organization_member_entity.py):** \
This allows the many-to-many relationship between organization and user tables.  
id  
organization_role  
User relationship:

- user_id: foreign key pointing to user.id
- user: back populates memberships

Organization relationship:

- organization_id: foreign key pointing to organization.id
- organization: back populates members

**[EDIT] OrganizationEntity (organization_entity.py):** \
The edit involves adding the secondary relationship with the user table through a one-to-many relationship with organization_membership.  
members: back populates organization from organization_membership  
users: back populates organizations from user

**[EDIT] UserEntity (user_entity.py):**  
The edit involves adding the secondary relationship with the organization table through a one-to-many relationship with organization_membership.  
memberships: back populates user from organization_membership  
organizations: back populates users from organization

## Implementation and Design Considerations

An important technical decision for the organization management’s roster is how to represent and store data about organization members. Entities for an organization and general CSXL user already exist, so we initially considered adding a new “roster” field to the organization entity to group all the members of an organization and make it easier for officers to manage members together. However, because this is actually a many-to-many relationship (where users can join multiple organizations under different roles and organizations will have many members), we found it necessary to create a new entity called OrganizationMembership that describes the relationship between users and organizations as “user has membership in organization.” While creating a new entity makes it more complex to track and organize different representations of data, we hope that the OrganizationMembership entity will make it easier in future development to access fields specific to a membership such as membership term, organization role, and special privileges for event creation.

Our UX design tradeoff was how to introduce the edit interface of the roster - whether it should be enabled at the same time that “edit organization details” is usually activated, or if it should have its own toggle. We ultimately chose its own toggle because conceptually to us, editing the roster is a more common and frequent action, while editing an organization’s details is very rarely done, and they are two different things, as a roster is just a transient component of an organization. Therefore, they should be represented by different UX actions.

## Getting Started

#### To work on the widget UI and service injections:

/frontend/organization/widgets/organization-roster.html, ts, css  
Define what gets passed (services, roster data) into the roster widget in the .ts file.

/frontend/organization/organization.module.ts  
Add the widget here to the module.

/frontend/organization/widgets/organization-details-info-card.html, ts, css  
The join method from the parent's service is injected into the ts file.

/frontend/organization/organization-details-component.ts  
The service is passed into the organization-details component, which inject it into the roster and detail widgets. Helper functions are defined here to bridge between service calls and widget events.

#### To work on the FastAPI service in frontend:

/frontend/organization/organization.model.ts  
The shape of the membership model is defined here under organizations. If there is a change in what gets passed in from the backend, update it here.

/frontend/organization/organization-roster.service.ts  
The service is separately defined here within the widget folder. Any API methods involving roster manipulation should be defined here.

#### To work on the python API in backend:

backend/api/organization.py  
API methods to access data concerning organizations. For the organization management system, this is where to add methods involving membership data on an organization's detail page.

backend/models/organization_membership.py  
Represents the model used by API for organization membership.

/backend/services/organization.py  
API service connected to the organization and organization membership tables in the Postgres database. This service acts on and returns data to the organization API backend.

#### To work on the database operations and representations:

/backend/entities/organization_membership_entity.py  
Database entity containing all relevant information about an organization membership. In addition to details from the organization and user tables, an OrganizationMembershipEntity can have specific attributes for organization role, membership term, and special privileges within the organization.

/backend/entities/organization.py  
Database entity representing information about an organization.

/backend/entities/user.py  
Database entity representing information about a CSXL user.
