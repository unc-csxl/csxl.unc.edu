import { Component, EventEmitter, Input, Output } from '@angular/core';
import { OrgRole, Profile } from '../../models.module';
import { FormControl } from '@angular/forms';
import { Observable, ReplaySubject } from 'rxjs';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';

@Component({
    selector: 'roster-add-member-card',
    templateUrl: './roster-add-member-card.widget.html',
    styleUrls: ['./roster-add-member-card.widget.css']
})
export class RosterAddMemberCard {

    @Input() selectedUser?: Profile;
    @Input() userLookup!: FormControl;
    @Input() filteredUsers!: ReplaySubject<Profile[]>;
    @Input() filteredUsers$!: Observable<Profile[]>;

    @Output() onChangeSelectedMember = new EventEmitter<void>();
    @Output() onOptionPressed = new EventEmitter<MatAutocompleteSelectedEvent>();
    @Output() onAddManagerPressed = new EventEmitter<Profile>();

    constructor() { }

    changeSelectedMember() {
        this.onChangeSelectedMember.emit();
    }

    onOptionSelected(event: MatAutocompleteSelectedEvent) {
        this.onOptionPressed.emit(event);
    }

    onAddManager() {
        this.onAddManagerPressed.emit(this.selectedUser);
    }

    // removeMemberButtonPressed(id: number) {
    //     this.onRemoveMemberButtonPressed.emit(id)
    // }

    // promoteMemberButtonPressed(orgRole: OrgRole) {
    //     this.onPromoteMemberButtonPressed.emit(orgRole)
    // }

    // demoteMemberButtonPressed(orgRole: OrgRole) {
    //     this.onDemoteMemberButtonPressed.emit(orgRole)
    // }
}