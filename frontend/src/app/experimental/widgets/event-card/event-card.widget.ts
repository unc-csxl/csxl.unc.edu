/**
 * The Event Card widget abstracts the implementation of each
 * individual event card from the whole event page.
 * 
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, Input } from '@angular/core';

@Component({
    selector: 'event-card',
    templateUrl: './event-card.widget.html',
    styleUrls: ['./event-card.widget.css']
})
export class EventCard {

    @Input() eventName!: string
    @Input() eventTimeText!: string
    @Input() eventOrganizationName!: string
    @Input() eventLocation!: string

    constructor() { }
}