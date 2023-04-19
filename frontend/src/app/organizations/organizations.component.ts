/** Constructs the Organizations page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { profileResolver } from '../profile/profile.resolver';
import { OrganizationsService } from './organizations.service';
import { OrganizationSummary, Profile } from '../models.module';
import { OrgDetailsService } from '../org-details/org-details.service';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent {

  /** Route information to be used in App Routing Module */
  public static Route = { 
    path: 'organizations',
    title: 'CS Organizations',
    component: OrganizationsComponent,
    canActivate: [],
    resolve: { profile: profileResolver } 
  }

  /** Store Observable list of Organizations */
  public organizations$: Observable<OrganizationSummary[]>;

  /** Store searchBarQuery */
  searchBarQuery = "";


  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;
  
  /** Stores the user permission value for current organization. */
  public permValues: Map<number, number> = new Map();

  constructor(private organizationService: OrganizationsService, iconRegistry: MatIconRegistry, sanitizer: DomSanitizer, protected orgDetailService: OrgDetailsService, private route: ActivatedRoute, protected snackBar: MatSnackBar) {
    /** Import Logos using MatIconRegistry */
    iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
    iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
    iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
    iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))
    
    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Retrieve Organizations using OrganizationsService */
    this.organizations$ = this.organizationService.getOrganizations();

    /** Retrieve all permission values for organizations */
    this.organizations$.subscribe((orgs) => {
      orgs.map((org) => {
        const filter = this.profile.organization_associations.filter(oa => oa.org_id == org.id);
        if(filter && filter.length > 0) {
          this.permValues.set(org.id!.valueOf(), filter[0].membership_type.valueOf());
        }
        else {
          this.permValues.set(org.id!.valueOf(), -1)
        }
      })
    })
    }
    
    /** Initialize the profile to be the currently-logged-in user's profile. */
    ngOnInit(): void {
      let profile = this.profile;
    }

  /**
   * Event handler to toggle the star status of an organization.
   */
  async starOrganization(orgId: Number): Promise<void> {
    
    // If user is an admin, they should not be able to unstar the organization.
    const filter = this.profile.organization_associations.filter(oa => oa.org_id == orgId);
    if(filter && filter.length > 0 && filter[0].membership_type.valueOf() >= 1) {

      // Open snack bar to notify user that the event was deleted.
      this.snackBar.open("You cannot unstar this organization because you are an admin.", "", { duration: 2000 })
    }
    else {
      if(this.profile && this.profile.first_name) {
        // Call the orgDetailsService's starOrganization() method.
        this.orgDetailService.starOrganization(orgId.valueOf());
          
        // Set slight delay so page reloads after API calls finish running.
        await new Promise(f => setTimeout(f, 200));

        // Reload the window to update the events.
        location.reload();
      }
    }
  }
}
