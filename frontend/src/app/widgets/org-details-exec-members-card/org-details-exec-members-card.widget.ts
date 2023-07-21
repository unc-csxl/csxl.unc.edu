import { Component, Input } from '@angular/core';
import { OrgRole } from 'src/app/models.module';

@Component({
    selector: 'org-details-exec-members-card',
    templateUrl: './org-details-exec-members-card.widget.html',
    styleUrls: ['./org-details-exec-members-card.widget.css']
})
export class OrgDetailsExecMembersCard {

    @Input() executives!: OrgRole[];

    constructor() {2}

}

