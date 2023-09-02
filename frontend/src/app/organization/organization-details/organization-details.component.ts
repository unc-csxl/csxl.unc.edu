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
import { Observable, map } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Organization, OrganizationService } from '../organization.service';
import { Profile, ProfileService } from '/workspace/frontend/src/app/profile/profile.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  let organizationId = route.params['id'];

  let organizationDetailSvc = inject(OrganizationService);
  let organization$ = organizationDetailSvc.getOrganization(organizationId);
  return organization$.pipe(map(organization => {
    if (organization) {
      return `${organization.name}`;
    } else {
      return "Organization Details"
    }
  }))
}

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {
  public static Route: Route = {
    path: ':id',
    component: OrganizationDetailsComponent,
    title: titleResolver,
    resolve: { profile: profileResolver }
  };

  public organization$: Observable<Organization>;
  public organization: Organization | undefined = undefined;
  id: string = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  constructor(
    private orgService: OrganizationService,
    private profileService: ProfileService,
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
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Load current route ID */
    this.route.params.subscribe(params => this.id = params["id"]);

    /** Retrieve Organization using OrgDetailsService */
    this.organization$ = this.orgService.getOrganization(this.id);
    this.organization$.subscribe(organization => this.organization = organization);

  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }
}