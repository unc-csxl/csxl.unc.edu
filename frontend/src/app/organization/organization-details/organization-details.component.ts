/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn, Route } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization } from '../organization.model';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import { organizationDetailResolver } from '../organization.resolver'

/** Injects the organization's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['organization'].name;
};

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {

  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    resolve: { profile: profileResolver, organization: organizationDetailResolver },
    children: [{ path: '', title: titleResolver, component: OrganizationDetailsComponent }]
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** The organization to show */
  public organization: Organization;

  /** Constructs the Organization Detail component */
  constructor(private route: ActivatedRoute, protected snackBar: MatSnackBar) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as { profile: Profile, organization: Organization };
    this.profile = data.profile;
    this.organization = data.organization;
  }
}