import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Organization, Profile } from '../../models.module';

@Component({
    selector: 'org-details-events-card',
    templateUrl: './org-details-events-card.widget.html',
    styleUrls: ['./org-details-events-card.widget.css']
})
export class OrgDetailsEventsCard {

    @Input() organization?: Organization;
    @Input() profile!: Profile;
    @Input() isAdmin: boolean = false;
    @Output() onDeleteEventButtonPressed = new EventEmitter<number>();

    constructor() { }

    deleteEventButtonPressed(id: number) {
        this.onDeleteEventButtonPressed.emit(id)
    }
}