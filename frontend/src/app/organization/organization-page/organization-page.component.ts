/**
 * The Organization Page Component serves as a hub for students to browse all of the CS
 * organizations at UNC. Students are also able to join public organizations, filter
 * based on interests, and access social media pages of organizations to stay up-to-date.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Signal, effect } from '@angular/core';
import { Organization } from '../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile, ProfileService } from '../../profile/profile.service';
import { NagivationAdminGearService } from '../../navigation/navigation-admin-gear.service';
import { OrganizationService } from '../organization.service';

@Component({
  selector: 'app-organization-page',
  templateUrl: './organization-page.component.html',
  styleUrls: ['./organization-page.component.css']
})
export class OrganizationPageComponent {
  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: '',
    title: 'Organizations',
    component: OrganizationPageComponent
  };

  /** Current search bar query on the organization page. */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores a reactive organizations list. */
  public organizations: Signal<Organization[]>;

  constructor(
    protected snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private profileService: ProfileService,
    private gearService: NagivationAdminGearService
  ) {
    this.profile = this.profileService.profile()!;
    this.organizations = this.organizationService.organizations;
  }

  /** Effect that shows the organization admin gear if the user is an admin for at least one organization.*/
  organizationGearEffect = effect(
    () => {
      if (this.organizationService.adminOrganizations().length > 0) {
        this.gearService.showAdminGear('', 'organizations/admin');
      }
    },
    { allowSignalWrites: true } // Needed to update the gear signal.
  );
}
