/**
 * The Event Model defines the shape of Event data retrieved from
 * the Event Service and the API.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Profile } from '../models.module';
import { Organization } from '../organization/organization.model';
import { PublicProfile } from '../profile/profile.service';

export enum RegistrationType {
  ATTENDEE,
  ORGANIZER
}

export interface EventRegistration {
  id: number | null;
  event_id: number;
  user_id: number;
  event: Event | null;
  user: Profile | null;
  is_organizer: boolean | null;
}

export interface EventOverviewJson {
  id: number;
  name: string;
  start: string;
  end: string;
  location: string;
  description: string;
  public: boolean;
  number_registered: number;
  registration_limit: number;
  organization_id: number;
  organization_slug: string;
  organization_icon: string;
  organization_name: string;
  organizers: PublicProfile[];
  user_registration_type: RegistrationType | null;
  image_url: string | null;
  override_registration_url: string | null;
}

export interface EventOverview {
  id: number | null;
  name: string;
  start: Date;
  end: Date;
  location: string;
  description: string;
  public: boolean;
  number_registered: number;
  organization_id: number;
  registration_limit: number;
  organization_slug: string;
  organization_icon: string;
  organization_name: string;
  organizers: PublicProfile[];
  user_registration_type: RegistrationType | null;
  image_url: string | null;
  override_registration_url: string | null;
}

export interface EventDraft {
  id: number | null;
  name: string;
  start: Date;
  end: Date;
  location: string;
  description: string;
  public: boolean;
  registration_limit: number;
  organization_slug: string;
  organizers: PublicProfile[];
  image_url: string | null;
  override_registration_url: string | null;
}

export const eventOverviewToDraft = (overview: EventOverview): EventDraft => {
  return {
    id: overview.id,
    name: overview.name,
    start: overview.start,
    end: overview.end,
    location: overview.location,
    description: overview.description,
    public: overview.public,
    registration_limit: overview.registration_limit,
    organization_slug: overview.organization_slug,
    organizers: overview.organizers,
    image_url: overview.image_url,
    override_registration_url: overview.override_registration_url
  };
};

/** Function that converts an EventJSON response model to an Event model.
 *  This function is needed because the API response will return certain
 *  objects (such as `Date`s) as strings. We need to convert this to
 *  TypeScript objects ourselves.
 */
export const parseEventOverviewJson = (
  responseModel: EventOverviewJson
): EventOverview => {
  return Object.assign({}, responseModel, {
    start: new Date(responseModel.start),
    end: new Date(responseModel.end)
  });
};

export interface EventStatusOverviewJson {
  featured: EventOverviewJson | null;
  registered: EventOverviewJson[];
}
export interface EventStatusOverview {
  featured: EventOverview | null;
  registered: EventOverview[];
}

export const parseEventStatusOverviewJson = (
  responseModel: EventStatusOverviewJson
): EventStatusOverview => {
  return Object.assign({}, responseModel, {
    featured: responseModel.featured
      ? parseEventOverviewJson(responseModel.featured!)
      : null,
    registered: responseModel.registered.map((registered) =>
      parseEventOverviewJson(registered)
    )
  });
};
