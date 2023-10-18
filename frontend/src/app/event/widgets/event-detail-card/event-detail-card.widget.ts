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
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
    selector: 'event-detail-card',
    templateUrl: './event-detail-card.widget.html',
    styleUrls: ['./event-detail-card.widget.css']
})
export class EventDetailCard {

    @Input() event!: Event

    constructor(protected snackBar: MatSnackBar) { }

    onShareButtonClick() {
        navigator.clipboard.writeText("https://csxl.unc.edu/events/" + this.event.id);
        this.snackBar.open("Event link copied to clipboard.", "", {duration: 3000})
    }
}