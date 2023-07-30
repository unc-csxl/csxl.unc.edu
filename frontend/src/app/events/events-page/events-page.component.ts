/**
 * The Events Page Component allows students see events hosted by CS organizations.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { EventsService } from '../events.service';
import { Observable } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { FormGroup, FormControl } from '@angular/forms';
import { Profile, Event, EventSummary, OrganizationSummary, Registration } from 'src/app/models.module';
import { OrganizationsService } from 'src/app/organizations/organizations.service';
import { ProfileService } from 'src/app/profile/profile.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-events-page',
  templateUrl: './events-page.component.html',
  styleUrls: ['./events-page.component.css']
})
export class EventsPageComponent {

  /** Store Observable list of Events */
  public events$: Observable<Event[]>;

  /** Store Observable list of Organizations */
  public organizationsList$: Observable<OrganizationSummary[]>;


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
    component: EventsPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver }
  }

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  public canRegisterMap: Map<number, boolean> = new Map();
  public canUnregisterMap: Map<number, boolean> = new Map();

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }

  /** Registers a user for the given event
   * @param eventId: number representing the id of the event the user should be registered for
   */
  register = async (eventId: number) => {
    if (this.profile.id !== null) {
      this.events$.subscribe(events => {
        const eventToRegister = events.filter(e => e.id == eventId)[0]

        this.eventsService.register(eventId, this.profile!.id!).subscribe(registration => {
          // Open snack bar to notify user that the registration was created.
          this.snackBar.open("Registered", "", { duration: 2000 })

          this.profileService.refreshProfile();
          this.profileService.profile$.subscribe(profile => {

            this.profile = profile!

            // Reload the window to update the registrations.
            this.canRegisterMap.set(eventId, this.canRegisterForEvent(eventToRegister))
            this.canUnregisterMap.set(eventId, this.canUnRegisterForEvent(eventToRegister))

          });
        })
      })
    } else {
      this.snackBar.open("Please fill out your profile information!", "", { duration: 2000 })
    }
  }

  /** Unregisters a user for the given event
   * @param eventId: number representing the id of the event the user should be unregistered for
   */
  unregister = async (eventId: number) => {
    if (this.profile.id !== null) {
      this.events$.subscribe(events => {
        const eventToUnregister = events.filter(e => e.id == eventId)[0]
        const registrationToDelete = this.profile.event_associations.filter(r => r.event_id == eventId && r.user_id == this.profile!.id!)[0]

        // this.profileService.deleteRegistration(eventId);
        this.eventsService.unregister(registrationToDelete.id!).subscribe(_ => {
          // Open snack bar to notify user that the registration was canceled.
          this.snackBar.open("Registration Canceled", "", { duration: 2000 })

          this.profileService.refreshProfile();
          this.profileService.profile$.subscribe(profile => {
            this.profile = profile!

            this.canRegisterMap.set(eventId, this.canRegisterForEvent(eventToUnregister))
            this.canUnregisterMap.set(eventId, this.canUnRegisterForEvent(eventToUnregister))
          });

        })
      })
    }
  }

  /** Returns whether or not the event is a past or current event
   * @param event_time: Date object representing the time of the event 
   * @returns {boolean}
   */
  checkCurrentEvent = (event_time: Date) => {
    if (new Date(event_time) < new Date()) {
      return false;
    }
    return true;
  }

  /** Returns whether or not a user is registered for an event
   * @param eventId: ID of the event
   * @returns {boolean}
   */
  checkIsRegistered = (eventId: number) => {

    // If a user is currently logged in, get their registrations and determine if the registration is valid
    if (this.profile) {
      // For each registration in the list of registrations
      for (let reg of this.profile!.event_associations) {
        // If the registration's event and user IDs match the desired event and user IDs
        if (reg.event_id == eventId && reg.user_id == this.profile!.id!) {
          return true;
        }
      }
    }
    return false;
  }

  constructor(route: ActivatedRoute, private eventsService: EventsService, private orgService: OrganizationsService, protected snackBar: MatSnackBar, private profileService: ProfileService) {
    /** Retrieve Events using EventsService */
    this.events$ = this.eventsService.getEvents();

    /** Retrieve Organizations using OrganizationsService */
    this.organizationsList$ = this.orgService.getOrganizations();

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    this.events$.subscribe(events => {
      events.forEach(event => {
        this.canRegisterMap.set(event.id!, this.canRegisterForEvent(event))
        this.canUnregisterMap.set(event.id!, this.canUnRegisterForEvent(event))
      })
    })
  }

  canRegisterForEvent = (event: Event) => {
    return this.checkCurrentEvent(event.time) && !this.checkIsRegistered(event.id!) && this.profile != null
  }

  canUnRegisterForEvent = (event: Event) => {
    return this.checkCurrentEvent(event.time) && this.checkIsRegistered(event.id!) && this.profile != null
  }
}