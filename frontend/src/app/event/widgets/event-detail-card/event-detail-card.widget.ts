/**
 * The Event Card widget abstracts the implementation of the
 * detail event card from the whole event page.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Organization } from 'src/app/organization/organization.service';
import { Event } from '../../event.service';

@Component({
    selector: 'event-detail-card',
    templateUrl: './event-detail-card.widget.html',
    styleUrls: ['./event-detail-card.widget.css']
})
export class EventDetailCard {

    @Input() event!: Event
    // @Input() eventName!: string
    // @Input() eventOrganization!: Organization
    // @Input() eventStartText!: string
    // @Input() eventEndText!: string
    // @Input() eventLocation!: string
    // @Input() eventDescription!: string
    // @Input() requiresPreregistration!: boolean
    // @Input() seatsRemaining!: number

    constructor() { }
}