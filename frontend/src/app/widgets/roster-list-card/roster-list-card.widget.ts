import { Component, EventEmitter, Input, Output } from '@angular/core';
import { OrgRole, Profile } from '../../models.module';

@Component({
    selector: 'roster-list-card',
    templateUrl: './roster-list-card.widget.html',
    styleUrls: ['./roster-list-card.widget.css']
})
export class RosterListCard {

    @Input() orgRoles!: OrgRole[];
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

    promoteMemberButtonPressed(orgRole: OrgRole) {
        this.onPromoteMemberButtonPressed.emit(orgRole)
    }

    demoteMemberButtonPressed(orgRole: OrgRole) {
        this.onDemoteMemberButtonPressed.emit(orgRole)
    }
}