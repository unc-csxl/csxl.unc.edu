/**
 * The Organization Page Component serves as a hub for students to browse all of the CS
 * organizations at UNC. Students are also able to join public organizations, filter
 * based on interests, and access social media pages of organizations to stay up-to-date.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit, Signal } from '@angular/core';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization } from '../organization.model';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';
import { NewOrganizationService } from '../new-organization.service';

@Component({
  selector: 'app-organization-page',
  templateUrl: './organization-page.component.html',
  styleUrls: ['./organization-page.component.css']
})
export class OrganizationPageComponent implements OnInit {
  /** Route information to be used in Organization Routing Module */
  public static Route = {
    path: '',
    title: 'CS Organizations',
    component: OrganizationPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver }
  };

  /** Store searchBarQuery */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  public organizations: Signal<Organization[]>;

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private organizationService: NewOrganizationService,
    private gearService: NagivationAdminGearService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
    };

    this.profile = data.profile;
    this.organizations = this.organizationService.organizations;
  }

  ngOnInit() {
    // Check for admin permissions
    this.gearService.showAdminGear(
      'organizations.*',
      '*',
      '',
      'organizations/admin'
    );
  }
}
