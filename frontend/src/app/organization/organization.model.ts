/**
 * The Organization Model defines the shape of Organization data
 * retrieved from the Organization Service and the API.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

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
  slug: string;
  shorthand: string;
  events: Event[] | null;
  members: OrganizationMembership[] | null;
}

/** Interface for Organization Membership (used in roster widget) */
export interface OrganizationMembership {
  id: number | null;
  user: Profile;
  organization_id: number;
  organization_slug: string;
  role: OrganizationRole;
}

enum OrganizationRole {
  PRESIDENT = 'President',
  OFFICER = 'Officer',
  MEMBER = 'Member',
  ADMIN = 'Member with Admin'
}
