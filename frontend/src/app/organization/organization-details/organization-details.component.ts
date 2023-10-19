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
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization } from '../organization.service';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import { organizationDetailResolver } from '../organization.resolver'

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['organization'].name;
};

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    resolve: { profile: profileResolver, organization: organizationDetailResolver },
    children: [{ path: '', title: titleResolver, component: OrganizationDetailsComponent }]
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;
  public organization: Organization;

  constructor(
    iconRegistry: MatIconRegistry,
    sanitizer: DomSanitizer,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar) {

    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as { profile: Profile, organization: Organization };
    this.profile = data.profile;
    this.organization = data.organization;
  }
}