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
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Organization, OrganizationsService } from '../organizations.service';
import { Profile, ProfileService } from 'src/app/profile/profile.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  let orgId = route.params['id'];

  let orgDetailSvc = inject(OrganizationsService);
  let org$ = orgDetailSvc.getOrganization(orgId);
  return org$.pipe(map(org => {
    if (org) {
      return `${org.name}`;
    } else {
      return "Organization Details"
    }
  }))
}

@Component({
  selector: 'app-org-details',
  templateUrl: './org-details.component.html',
  styleUrls: ['./org-details.component.css']
})
export class OrgDetailsComponent {
  public static Route: Route = {
    path: ':id',
    component: OrgDetailsComponent,
    title: titleResolver,
    resolve: { profile: profileResolver }
  };

  public organization$: Observable<Organization>;
  public organization: Organization | undefined = undefined;
  id: string = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  constructor(
    private orgService: OrganizationsService,
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
    this.organization$.subscribe(org => this.organization = org);

  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }
}