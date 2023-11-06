# Feature Permissions

> Written by Jade Keegan for the CSXL Web Application.<br> > _Last Updated: 11/3/2023_

## Introduction

This document specifies the permissions to be added for the various actions within the application that require special authorization. In the frontend of the application, these permissions may be added on the `Admin Role Details` page.

Each permission consists of an _action_ and a _resource_, both of which are strings. The action consists of the name of the corresponding feature service followed by an action such as create/view/update/delete (such as `organizations.create`). The resource specifies the path of the API route being operated on.

For more comprehensive information about how permissions work within the backend code, please refer to the document titled [auth.md](./auth.md).

## Organizations

| Action              | Resource                       | Permission                                          |
| ------------------- | ------------------------------ | --------------------------------------------------- |
| organization.create | organization                   | Create an organization to be added to the database. |
| organization.delete | organization                   | Delete an existing organization from the database.  |
| organization.update | organization/{organization_id} | Update information about an existing organization.  |

The table above defines permissions for the Organizations feature of the application. _Note that these are not fully implemented yet in the backend and frontend._

The `organization.create` and `organization.delete` permissions may be added to any Role in the application, but this should be done with caution, especially since deleting an organization will permanently delete it and its corresponding events from the database.

The `organization.update` permission should be added under a role for a particular organization with some `organization_id` corresponding to that organization. Roles for organizations are specified as follows: "Org: [*Organization Name/Slug*]".The resource must include the `organization_id` to ensure that only members of the organization have the ability to update it.

As an example, to add the `organization.update` permission to leaders of HackNC (which has an organization ID of 29), first find/create a role with the name _Org: HackNC_. On the role details page, input `organization.update` as the action for a new permission and `organization/29` as the resource and click **Grant**. Now, any user added to the _Org: HackNC_ role will have the ability to update HackNC's organization information!

## Events

| Action                     | Resource                       | Permission                                   |
| -------------------------- | ------------------------------ | -------------------------------------------- |
| organization.events.create | organization/{organization_id} | Create an event to be added to the database. |
| organization.events.delete | organization/{organization_id} | Delete an existing event from the database.  |
| organization.events.update | organization/{organization_id} | Update information about an existing event.  |

The table above defines permissions for the Events feature of the application.

These permissions require the `organization_id` in the resource string in order to ensure that a user may only alter events for the organization(s) they have permissions for. Similar to the `organization.update` permission, these permissions should be added under the Role for a specific Organization, and the `organization_id` in the resource string should correspond to that organization.

For example, to add all of these event management permissions to leaders of HackNC (which has an organization ID of 29), first find/create a role with the name _Org: HackNC_. On the role details page, input `organization.events.*` as the action for a new permission and `organization/29` as the resource and click **Grant**. Now, any user added to the _Org: HackNC_ role will have the ability to manage HackNC's events!
_\*Note that we use "\*" as a wild card character to encompass all of the actions (create/delete/update) since the leader of an organization should have full management permissions for the organization's events._

## Coworking

[TBA]
