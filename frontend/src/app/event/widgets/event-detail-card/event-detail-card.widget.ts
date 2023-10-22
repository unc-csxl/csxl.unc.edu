/**
 * The Event Detail Card widget abstracts the implementation of the
 * detail event card from the whole event page.
 *
 * @author Ajay Gandecha
 * @copyright 2023
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Event } from '../../event.model';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'event-detail-card',
    templateUrl: './event-detail-card.widget.html',
    styleUrls: ['./event-detail-card.widget.css']
})
export class EventDetailCard {

    /** The event for the event card to display */
    @Input() event!: Event

    /** Constructs the widget */
    constructor(protected snackBar: MatSnackBar) { }

    /** Handler for when the share button is pressed
     *  This function copies the permalink to the event to the user's
     *  clipboard.
     */
    onShareButtonClick() {
        // Write the URL to the clipboard
        navigator.clipboard.writeText("https://csxl.unc.edu/events/" + this.event.id);
        // Open a snackbar to alert the user
        this.snackBar.open("Event link copied to clipboard.", "", {duration: 3000})
    }
}
