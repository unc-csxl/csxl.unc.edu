import { Component, EventEmitter, Input, Output } from '@angular/core';
import { OrganizationSummary } from '../../models.module';

@Component({
    selector: 'profile-organizations-card',
    templateUrl: './profile-organizations-card.widget.html',
    styleUrls: ['./profile-organizations-card.widget.css']
})
export class ProfileOrganizationsCard {

    @Input() organizations!: OrganizationSummary[];
    @Output() onDeleteOrgMembershipButtonPressed = new EventEmitter<number>();

    constructor() {}

    deleteOrgMembershipButtonPressed(id: number) {
        this.onDeleteOrgMembershipButtonPressed.emit(id)
    }

    /** Helper function to build the URL for each organization.
   * @param id ID of the organization
   * @returns URL for the organization
   */
  routeBuilder = (id: number | null) => {
    return "/organization/" + id;
  }
}