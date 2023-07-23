/** Interface for Permission Type */
export interface Permission {
  id?: number;
  action: string;
  resource: string;
}

/** Interface for Profile Type */
export interface Profile {
  id: number | null;
  pid: number;
  onyen: string;
  first_name: string | null;
  last_name: string | null;
  email: string | null;
  pronouns: string | null;
  registered: boolean;
  role: number;
  permissions: Permission[];    
  events:Event[];
  github: string | null;
  github_id: number | null;
  github_avatar: string | null;
  event_associations: Registration[];
  organizations: OrganizationSummary[];
  organization_associations: OrgRole[];
}

/** Interface for UserSummary Type (used on frontend for user requests) */
export interface UserSummary {
  id: number | null;
  pid: number;
  onyen: string;
  first_name: string | null;
  last_name: string | null;
  email: string | null;
  pronouns: string | null;
  permissions: Permission[];
}

/** Interface for Organization Type (used on frontend for organization detail) */
export interface Organization {
  id: number | null;
  name: string;
  logo: string;
  short_description: string;
  long_description: string;
  website: string;
  email: string;
  instagram: string;
  linked_in: string;
  youtube: string;
  heel_life: string;
  events: EventSummary[];
  users: UserSummary[];
  user_associations: OrgRole[];
}

/** Interface for OrganizationSummary Type (used on frontend for organization requests) */
export interface OrganizationSummary {
  id: number | null;
  name: string;
  slug: string;
  logo: string;
  short_description: string;
  long_description: string;
  website: string;
  email: string;
  instagram: string;
  linked_in: string;
  youtube: string;
  heel_life: string;
}

/** Interface for OrgRole Type (defines relationships between users and organizations) */
export interface OrgRole {
  id: number| null;
  user_id: number;
  org_id: number;
  membership_type: number;
  organization: OrganizationSummary | null;
  user: UserSummary | null;
}
/** Interface for OrgRole Type (defines relationships between users and organizations) */
export interface OrgRoleSummary {
  id: number| null;
  user_id: number;
  org_id: number;
  membership_type: number;
}

/** Interface for Event Type (used on frontend for event requests) */
export interface Event {
  id: number | null;
  name: string;
  time: Date;
  location: string;
  description: string;
  public: Boolean;
  org_id: number;
  organization: OrganizationSummary;
  users: UserSummary[];
  user_associations: Registration[];
}

/** Interface for EventSummary Type (used on frontend for creating events) */
export interface EventSummary {
  id: number | null;
  name: string;
  time: Date;
  location: string;
  description: string;
  public: Boolean;
  org_id: number;
}

/** Interface for Registration Type (defines relationships between users and events) */
export interface Registration {
  id: number | null;
  user_id: number;
  event_id: number;
  status: number;
  event: EventSummary;
  user: UserSummary;
}

/** Interface for RegistrationSummary Type (used on frontend for registration requests) */
export interface RegistrationSummary {
  id: number | null;
  user_id: number;
  event_id: number;
  status: number;
}

/** Interface for Organization Type */
export interface Organization {
  id: number | null
  slug: string
  name: string
  logo: string
  short_description: string
  long_description: string
  website: string
  email: string
  instagram: string
  linked_in: string
  youtube: string
  heel_life: string
}