import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable, Subscription, tap } from 'rxjs';
import { OrgDetailsService } from './org-details.service';
import { Organization, OrgRole, Profile } from '../models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '../profile/profile.resolver';

@Component({
  selector: 'app-org-details',
  templateUrl: './org-details.component.html',
  styleUrls: ['./org-details.component.css']
})
export class OrgDetailsComponent {
  public static Route: Route = {
    path: 'organization/:id',
    component: OrgDetailsComponent, 
    title: 'Organization Details', 
    resolve: { profile: profileResolver }
  };

  public organization$: Observable<Organization>;
  public organization: Organization | undefined = undefined;
  id: string = '';

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;
  
  /** Stores the user permission value for current organization. */
  public permValue: number = -1;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  /** Stores executives of the current organization */
  public executives: OrgRole[] = [];

  constructor(private orgDetailsService: OrgDetailsService, iconRegistry: MatIconRegistry, sanitizer: DomSanitizer, private route: ActivatedRoute, protected snackBar: MatSnackBar) {
    /** Import Logos using MatIconRegistry */
    iconRegistry.addSvgIcon('instagram', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/instagram.svg'));
    iconRegistry.addSvgIcon('github', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/github.svg'));
    iconRegistry.addSvgIcon('linkedin', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/linkedin.svg'))
    iconRegistry.addSvgIcon('youtube', sanitizer.bypassSecurityTrustResourceUrl('https://simpleicons.org/icons/youtube.svg'))
    
    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;
    
    /** Load current route ID */
    this.route.params.subscribe( params => this.id=params["id"]);

    /** Retrieve Organization using OrgDetailsService */ 
    this.organization$ = this.orgDetailsService.getOrganization(this.id);
    this.organization$.subscribe(org => this.organization = org);
    this.organization$.subscribe(org => {
      org.user_associations.forEach((association) => {
          if(association.membership_type >= 1) {
              this.executives.push(association);
          }
      })
    })

    /** Set permission value if profile exists */
    if(this.profile) {
      let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.id);
      if(assocFilter.length > 0) {
        this.permValue = assocFilter[0].membership_type;
        this.adminPermission = (this.permValue >= 2);
      }
    }
  }

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }

  /** Event handler to toggle the star status of an organization. */
  starOrganization = async () => {
    
    // If user is an admin, they should not be able to unstar the organization.
    if(this.adminPermission) {

      // Open snack bar to notify user that the event was deleted.
      this.snackBar.open("You cannot unstar this organization because you are an admin.", "", { duration: 2000 })
    }
    else {
      if(this.profile && this.profile.first_name) {
        // Call the orgDetailsService's starOrganization() method.
        this.orgDetailsService.starOrganization(+this.id);
          
        // Set slight delay so page reloads after API calls finish running.
        await new Promise(f => setTimeout(f, 100));

        // Reload the window to update the events.
        location.reload();
      }
    }
  }

  /** Event handler to delete an event.
   * @param event_id: Number representing the event to be deleted.
   * @returns {void}
   */
  deleteEvent = async (event_id: number) => {
    // Call the orgDetailsService's deleteEvent() method.
    this.orgDetailsService.deleteEvent(event_id);

      // Open snack bar to notify user that the event was deleted.
      this.snackBar.open("Deleted event", "", { duration: 2000 })
      await new Promise(f => setTimeout(f, 750));
   
    // Reload the window to update the events.
    location.reload();
  }
}