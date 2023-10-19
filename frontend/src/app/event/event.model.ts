/**
 * The Event Model defines the shape of Event data retrieved from
 * the Event Service and the API.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Organization } from '../organization/organization.service';

/** Interface for Event Type (used on frontend for event detail) */
export interface Event {
    id: number | null;
    name: string;
    time: Date;
    location: string;
    description: string;
    public: boolean;
    organization_id: number;
    organization: Organization;
}