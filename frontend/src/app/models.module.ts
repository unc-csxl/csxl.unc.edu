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
  events:EventSummary[];
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
  id: Number | null;
  name: String;
  logo: String;
  short_description: String;
  long_description: String;
  website: String;
  email: String;
  instagram: String;
  linked_in: String;
  youtube: String;
  heel_life: String;
  events: EventSummary[];
  users: UserSummary[];
  user_associations: OrgRole[];
}

/** Interface for OrganizationSummary Type (used on frontend for organization requests) */
export interface OrganizationSummary {
  id: Number | null;
  name: String;
  logo: String;
  short_description: String;
  long_description: String;
  website: String;
  email: String;
  instagram: String;
  linked_in: String;
  youtube: String;
  heel_life: String;
}

/** Interface for OrgRole Type (defines relationships between users and organizations) */
export interface OrgRole {
  id: Number| null;
  user_id: Number;
  org_id: Number;
  membership_type: Number;
  organization: OrganizationSummary | null;
  user: UserSummary | null;
}
/** Interface for OrgRole Type (defines relationships between users and organizations) */
export interface OrgRoleSummary {
  id: Number| null;
  user_id: Number;
  org_id: Number;
  membership_type: Number;
}

/** Interface for EventSummary Type (used on frontend for event requests) */
export interface EventSummary {
  id: Number | null;
  name: string;
  time: Date;
  location: string;
  description: string;
  public: Boolean;
  org_id: Number;
  organization: OrganizationSummary; 
}

export interface EventSummary2 {
  id: Number | null;
  name: string;
  time: Date;
  location: string;
  description: string;
  public: Boolean;
  org_id: Number;
}

/** Interface for Registration Type (defines relationships between users and events) */
export interface Registration {
  id: Number | null;
  user_id: Number;
  event_id: Number;
  status: Number;
  event: EventSummary;
  user: UserSummary;
}
