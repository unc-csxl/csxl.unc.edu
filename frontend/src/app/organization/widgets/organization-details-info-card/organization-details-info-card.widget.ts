import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.service';
import { Profile } from 'src/app/profile/profile.service';

@Component({
    selector: 'organization-details-info-card',
    templateUrl: './organization-details-info-card.widget.html',
    styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard {

    @Input() organization?: Organization;
    @Input() profile?: Profile;

    constructor() {}

}

