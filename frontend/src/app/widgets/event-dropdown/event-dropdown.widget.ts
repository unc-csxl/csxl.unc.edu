import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Event } from '../../models.module';

@Component({
    selector: 'event-dropdown',
    templateUrl: './event-dropdown.widget.html',
    styleUrls: ['./event-dropdown.widget.css']
})
export class EventDropdown {

    @Input() event!: Event;
    @Input() canRegister: boolean = true;
    @Input() canUnregister: boolean = true;

    @Output() onRegisterButtonPressed = new EventEmitter<number>();
    @Output() onUnregisterButtonPressed = new EventEmitter<number>();

    constructor() {}

    registerButtonPressed(id: number) {
        this.onRegisterButtonPressed.emit(id)
    }

    unregisterButtonPressed(id: number) {
        this.onUnregisterButtonPressed.emit(id)
    }
}