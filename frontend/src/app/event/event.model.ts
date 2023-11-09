/**
 * The Event Model defines the shape of Event data retrieved from
 * the Event Service and the API.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Organization } from '../organization/organization.model';

/** Interface for Event Type (used on frontend for event detail) */
export interface Event {
  id: number | null;
  name: string;
  time: Date;
  location: string;
  description: string;
  public: boolean;
  organization_id: number | null;
  organization: Organization | null;
}

/** Interface for the Event JSON Response model
 *  Note: The API returns object data, such as `Date`s, as strings. So,
 *  this interface models the data directly received from the API. It is
 *  the job of the `parseEventJson` function to convert it to the `Event` type
 */
export interface EventJson {
  id: number | null;
  name: string;
  time: string;
  location: string;
  description: string;
  public: boolean;
  organization_id: number | null;
  organization: Organization | null;
}

/** Function that converts an EventJSON response model to an Event model.
 *  This function is needed because the API response will return certain
 *  objects (such as `Date`s) as strings. We need to convert this to
 *  TypeScript objects ourselves.
 */
export const parseEventJson = (eventJson: EventJson): Event => {
  return Object.assign({}, eventJson, { time: new Date(eventJson.time) });
};
