import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EventSummary } from '../../models.module';

@Component({
    selector: 'profile-events-card',
    templateUrl: './profile-events-card.widget.html',
    styleUrls: ['./profile-events-card.widget.css']
})
export class ProfileEventsCard {

    @Input() events!: EventSummary[];
    @Output() onCancelRegistrationButtonPressed = new EventEmitter<number>();

    constructor() {}

    cancelRegistrationButtonPressed(id: number) {
        this.onCancelRegistrationButtonPressed.emit(id)
    }
}