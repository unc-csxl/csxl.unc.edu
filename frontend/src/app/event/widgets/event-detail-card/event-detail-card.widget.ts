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
import { EventService } from '../../event.service';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';

@Component({
    selector: 'event-detail-card',
    templateUrl: './event-detail-card.widget.html',
    styleUrls: ['./event-detail-card.widget.css']
})
export class EventDetailCard {

    /** The event for the event card to display */
    @Input() event!: Event

    /** Constructs the widget */
    constructor(protected snackBar: MatSnackBar, private eventService: EventService, private permission: PermissionService) { }

    checkPermissions(): Observable<boolean> {
        return this.permission.check('organization.events.manage', `organization/${this.event.organization_id!}`);
    }

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

    /** Delete the given event object using the Event Service's deleteEvent method
     * @param event: Event representing the updated event
     * @returns void
     */
    deleteEvent(event: Event): void {
        this.eventService.deleteEvent(event);
        this.snackBar.open("Event Deleted", "", { duration: 2000 })
    }
}
