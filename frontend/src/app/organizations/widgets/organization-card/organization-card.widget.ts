import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Organization } from '../../organizations.service';
import { Profile } from 'src/app/profile/profile.service';

@Component({
    selector: 'organization-card',
    templateUrl: './organization-card.widget.html',
    styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {

    @Input() organization!: Organization
    @Input() profile?: Profile
    @Input() profilePermissions!: Map<number, number>
    //@Output() onStarClicked = new EventEmitter<number>();

    constructor() { }

    // starClicked() {
    //     this.onStarClicked.emit(this.organization!.id!);
    // }
}


