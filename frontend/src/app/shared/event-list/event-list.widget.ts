/**
 * The Event List widget abstracts the implementation of the
 * event list from the page.
 * 
 * NOTE: This widget is in the Shared module because it is
 * used both by events and organizations.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Event } from '../../event/event.model';

@Component({
    selector: 'event-list',
    templateUrl: './event-list.widget.html',
    styleUrls: ['./event-list.widget.css']
})
export class EventList {

    /** The event for the event card to display */
    @Input() eventsPerDay: [string, Event[]][] = [];

    /** Store the selected Event */
    @Input() selectedEvent: Event | null = null;

    /** Whether or not to disable the links on the page */
    @Input() disableLinks: boolean = false;

    @Input() showHeader: boolean = false;

    @Output() onCardClicked: EventEmitter<Event> = new EventEmitter()

    /** Constructs the widget */
    constructor() { }
}
