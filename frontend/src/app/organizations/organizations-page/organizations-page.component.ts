/**
 * The Organization Page Component serves as a hub for students to browse all of the CS
 * organizations at UNC. Students are also able to join public organizations, filter
 * based on interests, and access social media pages of organizations to stay up-to-date.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { ChangeDetectorRef, Component } from '@angular/core';
import { Observable } from 'rxjs';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Organization, OrganizationsService } from '../organizations.service';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Profile, ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-organizations-page',
  templateUrl: './organizations-page.component.html',
  styleUrls: ['./organizations-page.component.css']
})
export class OrganizationsPageComponent {

  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'CS Organizations',
    component: OrganizationsPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver }
  }

  /** Store Observable list of Organizations */
  public organizations$: Observable<Organization[]>;

  /** Store searchBarQuery */
  public searchBarQuery = "";

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current organization. */
  public permValues: Map<number, number> = new Map();

  constructor(
    private organizationService: OrganizationsService,
    private profileService: ProfileService,
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
  ) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Retrieve Organizations using OrganizationsService */
    this.organizations$ = this.organizationService.getOrganizations();
  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }
}
