
Events Service
- checkIsRegistered: Returns whether or not the user is registered for an event
- getEvents: Returns all event entries from the backend database table
- register: Create a registration from the backend
- getEvent: Returns the event object from the backend database table
- updateEvent: Returns the updated event object from the backend database table

Organization Service 
- getOrganizations: Returns all organization entries from the backend database table
- getOrganization: Returns the organization object from the backend database table
- updateOrganization: Returns the updated organization object from the backend database table
- getOrganizationDetail: Returns an Observable Organization based on the given id
- create: Creates an event in the backend table
- toggleOrganizationMembership: Toggles the membership status of a user for an organization
- deleteEvent: Delete an event that the organization is hosting
- getRolesForOrganization: Returns the organization roles for an organization
- deleteRoleFromOrganization: Delete an organization role based on the role's ID
- promoteRole: Promotes a role
- demoteRole: Demote a role

Profile Service
- refreshProfile: *None*
- put: Updates the profile and returns the updated version of the profile
- search: Gets and returns a profile
- getUserOrganizations: Returns all organization entries for the current user
- getUserEvents: Returns all event entries for the current user
- deleteRegistration: Delete a registration from the backend
- deleteOrgMembership: Delete an org role from the backend
- getGitHubOAuthLoginURL: *GitHub*
- unlinkGitHub: *GitHub*