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

export const parseEventJson = (eventJson: EventJson[]): Event[] => {
    return eventJson.map((json) => Object.assign({}, json, { time: new Date(json.time) }));
};