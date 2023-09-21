/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, inject } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, ResolveFn, Route } from '@angular/router';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { map } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization, OrganizationService } from '../organization.service';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import { organizationResolver } from '/workspace/frontend/src/app/organization/organization.resolver'

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  let organizationSlug = route.params['slug'];

  let organizationDetailSvc = inject(OrganizationService);
  let organization$ = organizationDetailSvc.getOrganization(organizationSlug);
  return organization$.pipe(map(organization => {
    if (organization) {
      return `${organization.name}`;
    }
    else {
      return "Organization Details"
    }
}));
}

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    title: titleResolver,
    resolve: { profile: profileResolver, organization: organizationResolver },
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;
  public organization: Organization;

  constructor(
    iconRegistry: MatIconRegistry,
    sanitizer: DomSanitizer,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar) {
    /** Import Logos using MatIconRegistry */
    iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
    iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
    iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
    iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))

    /** Get currently-logged-in user. */
    const data = this.route.snapshot.data as { profile: Profile, organization: Organization };
    this.profile = data.profile;
    this.organization = data.organization;
  }
}