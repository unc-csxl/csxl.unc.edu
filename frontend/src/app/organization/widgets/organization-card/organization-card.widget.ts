import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.service';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';

@Component({
    selector: 'organization-card',
    templateUrl: './organization-card.widget.html',
    styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {

    @Input() organization!: Organization
    @Input() profile?: Profile
    @Input() profilePermissions!: Map<number, number>

    constructor() { }
}


