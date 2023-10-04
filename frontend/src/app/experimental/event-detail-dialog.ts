import { Component, HostListener, Inject } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { Organization } from '../organization/organization.service';
import { Subscription, map } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { EventDetailData } from './experimental.component';


@Component({
    selector: 'event-detail-dialog',
    template: `
        <event-detail-card [eventName]="data.name" [eventOrganization]="data.organization"
            [eventStartText]="data.startText" [eventEndText]="data.endText"
            [eventLocation]="data.location"
            [eventDescription]="data.description"
            [requiresPreregistration]="data.requiresPreregistration" />
    `
})
export class EventDetailDialog {
    constructor(
        public dialogRef: MatDialogRef<EventDetailDialog>,
        @Inject(MAT_DIALOG_DATA) public data: EventDetailData,
    ) { }

    onNoClick(): void {
        this.dialogRef.close();
    }
}