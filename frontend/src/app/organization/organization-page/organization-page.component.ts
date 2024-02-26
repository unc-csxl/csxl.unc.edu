/**
 * The Organization Page Component serves as a hub for students to browse all of the CS
 * organizations at UNC. Students are also able to join public organizations, filter
 * based on interests, and access social media pages of organizations to stay up-to-date.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, OnInit } from '@angular/core';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization } from '../organization.model';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import { organizationResolver } from '../organization.resolver';
import { NagivationAdminGearService } from 'src/app/navigation/navigation-admin-gear.service';

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
    resolve: { profile: profileResolver, organizations: organizationResolver }
  };

  /** Store Observable list of Organizations */
  public organizations: Organization[];

  /** Store searchBarQuery */
  public searchBarQuery = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current organization. */
  public permValues: Map<number, number> = new Map();

  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    private gearService: NagivationAdminGearService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      organizations: Organization[];
    };
    this.profile = data.profile;
    this.organizations = data.organizations;
  }

  ngOnInit() {
    let userPermissions = this.profile.permissions;
    if (userPermissions.length !== 0) {
      if (userPermissions[0].resource === '*') {
        this.gearService.showAdminGear(
          'organizations.*',
          '*',
          '',
          'organizations/admin'
        );
      } else {
        let organizationPermissions = userPermissions.filter((element) =>
          element.resource.includes('organization')
        );
        if (organizationPermissions.length !== 0) {
          this.gearService.showAdminGear(
            'organizations.*',
            organizationPermissions[0].resource,
            '',
            'organizations/admin'
          );
        }
      }
    }
  }
}
