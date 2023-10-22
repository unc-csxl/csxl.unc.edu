/**
 * The Event List widget abstracts the implementation of the
 * event list from the page.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Event } from '../../event/event.model';

@Component({
    selector: 'event-list',
    templateUrl: './event-list.widget.html',
    styleUrls: ['./event-list.widget.css']
})
export class EventList {

    /** The event for the event card to display */
    @Input() event!: Event

    /** Constructs the widget */
    constructor() { }
}
