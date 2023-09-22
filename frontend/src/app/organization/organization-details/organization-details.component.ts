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
    resolve: { profile: profileResolver }
  };

  public organization$: Observable<Organization>;
  public organization: Organization | undefined = undefined;
  slug: string = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  constructor(
    private orgService: OrganizationService,
    iconRegistry: MatIconRegistry,
    sanitizer: DomSanitizer,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Load current route slug */
    this.route.params.subscribe(params => this.slug = params["slug"]);

    /** Retrieve Organization using OrgDetailsService */
    this.organization$ = this.orgService.getOrganization(this.slug);
    this.organization$.subscribe(organization => this.organization = organization);

  }
}