import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EventSummary } from '../../models.module';

@Component({
    selector: 'profile-event-dropdown',
    templateUrl: './profile-event-dropdown.widget.html',
    styleUrls: ['./profile-event-dropdown.widget.css']
})
export class ProfileEventDropdown {

    @Input() event!: EventSummary;
    @Input() isCurrent: boolean = true;
    @Input() showCancelButton: boolean = true;
    @Input() isAdmin: boolean = false;

    @Output() onCancelRegistrationButtonPressed = new EventEmitter<number>();
    @Output() onDeleteEventButtonPressed = new EventEmitter<number>();

    constructor() {}

    cancelRegistrationButtonPressed(id: number) {
        this.onCancelRegistrationButtonPressed.emit(id)
    }

    deleteEventButtonPressed(id: number) {
        this.onDeleteEventButtonPressed.emit(id)
    }
}