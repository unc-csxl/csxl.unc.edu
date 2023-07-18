import { Component, EventEmitter, Input, Output } from '@angular/core';
import { OrganizationSummary, Profile } from 'src/app/models.module';

@Component({
    selector: 'organization-card',
    templateUrl: './organization-card.widget.html',
    styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {

    @Input() organization!: OrganizationSummary
    @Input() profile?: Profile
    @Input() profilePermissions!: Map<number, number>
    @Output() onStarClicked = new EventEmitter<number>();

    constructor() {}

    starClicked() {
        this.onStarClicked.emit(this.organization!.id!);
    }
}


