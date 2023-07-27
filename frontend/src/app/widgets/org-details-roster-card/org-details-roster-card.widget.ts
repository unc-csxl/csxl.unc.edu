import { Component, Input } from '@angular/core';
import { OrgRole, Profile } from 'src/app/models.module';

@Component({
    selector: 'org-details-roster-card',
    templateUrl: './org-details-roster-card.widget.html',
    styleUrls: ['./org-details-roster-card.widget.css']
})
export class OrgDetailsRosterCard {

    @Input() membersCount: number = 0;
    @Input() profile!: Profile;
    @Input() organizationId!: number;

    constructor() { }
}
