import { Component, Input } from '@angular/core';
import { Organization } from '../../organizations.service';
import { Profile } from 'src/app/profile/profile.service';

@Component({
    selector: 'org-details-info-card',
    templateUrl: './org-details-info-card.widget.html',
    styleUrls: ['./org-details-info-card.widget.css']
})
export class OrgDetailsInfoCard {

    @Input() organization?: Organization;
    @Input() profile?: Profile;
    // @Input() isAdmin: boolean = false;

    constructor() {}
}

