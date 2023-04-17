/** Constructs the Events page and stores/retrieves any necessary data for it. */

import { Component } from '@angular/core';
import { profileResolver } from '../profile/profile.resolver';
import { EventsService } from './events.service';
import { Observable } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { FormGroup, FormControl } from '@angular/forms';
import { Profile, EventSummary, OrganizationSummary, RegistrationSummary } from 'src/app/models.module';
import { OrganizationsService } from '../organizations/organizations.service';
import { ProfileService } from '../profile/profile.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.css']
})
export class EventsComponent {

  /** Store Observable list of Events */
  public events$: Observable<EventSummary[]>;

  /** Store Observable list of Organizations */
  public organizationsList$: Observable<OrganizationSummary[]>;

  /** Store Observable list of Registrations */
  public registrations: EventSummary[] = [];

  /** Store searchBarQuery */
  searchBarQuery = "";

  /** Store selected organizations */
  organizations = new FormControl([]);

  /** Store date range **/
  range = new FormGroup({
    start: new FormControl<Date | null>(new Date()),
    end: new FormControl<Date | null>(new Date(new Date().getTime() + 7 * 24 * 60 * 60 * 1000)),
  });

  /** Reset Button Functionality */
  reset = () => {
    this.searchBarQuery = "";
    this.range = new FormGroup({
      start: new FormControl<Date | null>(new Date()),
      end: new FormControl<Date | null>(new Date(new Date().getTime() + 7 * 24 * 60 * 60 * 1000)),
    });
    this.organizations = new FormControl([]);
  }

  /** Route information to be used in App Routing Module */
  public static Route = { 
    path: 'events',
    title: 'Events',
    component: EventsComponent,
    canActivate: [],
    resolve: { profile: profileResolver } 
  }

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

   /** Initialize the profile to be the currently-logged-in user's profile. */
   ngOnInit(): void {
    let profile = this.profile;
  }

  /** Registration Functionality */
  register = async (eventId: Number) => {
    this.eventsService.register(eventId);
    
    // Open snack bar to notify user that the organization membership was deleted.
    this.snackBar.open("Registered", "", { duration: 2000 })
    await new Promise(f => setTimeout(f, 750));

    // Reload the window to update the organizations.
    location.reload();
  }

  constructor(route: ActivatedRoute, private eventsService: EventsService, private orgService: OrganizationsService, protected snackBar: MatSnackBar, private profileService: ProfileService) {
    /** Retrieve Events using EventsService */
    this.events$ = this.eventsService.getEvents();
    
    /** Retrieve Organizations using OrganizationsService */
    this.organizationsList$ = this.orgService.getOrganizations();

    /** Retrieve User Registrations using ProfileService */
    this.registrations = this.profileService.getUserEvents();

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;
    }

}