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
import { Profile, Event, EventSummary, OrganizationSummary } from 'src/app/models.module';
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
    component: EventsPageComponent,
    canActivate: [],
    resolve: { profile: profileResolver }
  }

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Initialize the profile to be the currently-logged-in user's profile. */
  ngOnInit() {
    let profile = this.profile;
  }

  /** Registers a user for the given event
   * @param eventId: number representing the id of the event the user should be registered for
   */
  register = async (eventId: number) => {
    if (this.profile.id !== null) {
      this.eventsService.register(eventId);

      // Open snack bar to notify user that the registration was created.
      this.snackBar.open("Registered", "", { duration: 2000 })
      await new Promise(f => setTimeout(f, 750));

      // Reload the window to update the registrations.
      location.reload();
    } else {
      this.snackBar.open("Please fill out your profile information!", "", { duration: 2000 })
    }
  }

  /** Unregisters a user for the given event
   * @param eventId: number representing the id of the event the user should be unregistered for
   */
  unregister = async (eventId: number) => {
    if (this.profile.id !== null) {
      this.profileService.deleteRegistration(eventId);

      // Open snack bar to notify user that the registration was canceled.
      this.snackBar.open("Registration Canceled", "", { duration: 2000 })
      await new Promise(f => setTimeout(f, 750));

      // Reload the window to update the events.
      location.reload();
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
    return this.eventsService.checkIsRegistered(eventId);
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