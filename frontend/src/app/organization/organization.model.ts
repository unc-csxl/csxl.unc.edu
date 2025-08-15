/**
 * The Organization Model defines the shape of Organization data
 * retrieved from the Organization Service and the API.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Term } from '../academics/academics.models';
import { Profile } from '../profile/profile.service';

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
  public: boolean;
  join_type: OrganizationJoinType | null;
  slug: string;
  shorthand: string;
  events: Event[] | null;
  members: OrganizationMembership[] | null;
}

/** Interface for Organization Membership (used in roster widget) */
export interface OrganizationMembership {
  id: number;
  user: Profile;
  organization_id: number;
  organization_slug: string;

  title: string;
  permission_level: OrganizationMembershipPermissionLevel;
  status: OrganizationMembershipStatus;
  term: Term;
  selected_title?: string; // For editing purposes
  selected_permission_level?: OrganizationMembershipPermissionLevel; // For editing purposes
  checked?: boolean; // For editing purposes
}

export enum OrganizationMembershipStatus {
  ACTIVE = 'Active',
  PENDING = 'Membership pending'
}

export enum OrganizationMembershipPermissionLevel {
  MEMBER = 'Member',
  ADMIN = 'Admin'
}

export enum OrganizationJoinType {
  OPEN = 'Open',
  APPLY = 'Apply',
  CLOSED = 'Closed'
}
