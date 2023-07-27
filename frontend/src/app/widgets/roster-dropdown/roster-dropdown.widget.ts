import { Component, EventEmitter, INJECTOR, Input, Output } from '@angular/core';
import { Event, OrgRole, Profile } from '../../models.module';

@Component({
    selector: 'roster-dropdown',
    templateUrl: './roster-dropdown.widget.html',
    styleUrls: ['./roster-dropdown.widget.css']
})
export class RosterDropdown {

    @Input() orgRole!: OrgRole;
    @Input() isManager!: boolean;
    @Input() isAdmin!: boolean;
    @Input() profile!: Profile;

    @Output() onRemoveMemberButtonPressed = new EventEmitter<number>();
    @Output() onPromoteMemberButtonPressed = new EventEmitter<OrgRole>();
    @Output() onDemoteMemberButtonPressed = new EventEmitter<OrgRole>();

    constructor() { }

    removeMemberButtonPressed(id: number) {
        this.onRemoveMemberButtonPressed.emit(id)
    }

    promoteMemberButtonPressed() {
        this.onPromoteMemberButtonPressed.emit(this.orgRole)
    }

    demoteMemberButtonPressed() {
        this.onDemoteMemberButtonPressed.emit(this.orgRole)
    }

    membershipTypeText = (membership: number) => {
        if (membership == 0) return "Member";
        if (membership == 1) return "Manager";
        if (membership == 2) return "Admin";
        return "Unknown";
    }
}