/**
 * The Event Editor Component allows users to edit information
 * about events which are publically displayed on the Events page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventService } from '../event.service';
import {
  Profile,
  ProfileService,
  PublicProfile
} from '../../profile/profile.service';
import { eventResolver } from '../event.resolver';
import { DatePipe } from '@angular/common';
import { OrganizationService } from 'src/app/organization/organization.service';
import { eventEditorGuard } from './event-editor.guard';
import { EventOverview, eventOverviewToDraft } from '../event.model';

@Component({
  selector: 'app-event-editor',
  templateUrl: './event-editor.component.html',
  styleUrls: ['./event-editor.component.css']
})
export class EventEditorComponent {
  /** Route information to be used in Event Routing Module */
  public static Route: Route = {
    path: ':orgid/:id/edit',
    component: EventEditorComponent,
    title: 'Event Editor',
    canActivate: [eventEditorGuard],
    resolve: {
      event: eventResolver
    }
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the event.  */
  public event: EventOverview;

  /** Store organizers */
  public organizers: PublicProfile[];

  /** Event Editor Form */
  public eventForm = this.formBuilder.group({
    name: new FormControl('', [Validators.required]),
    time: new FormControl(
      this.datePipe.transform(new Date(), 'yyyy-MM-ddTHH:mm'),
      [Validators.required]
    ),
    image_url: new FormControl(''),
    location: new FormControl('', [Validators.required]),
    description: new FormControl('', [
      Validators.required,
      Validators.maxLength(2000)
    ]),
    public: new FormControl(false, [Validators.required]),
    registration_limit: new FormControl(0, [
      Validators.required,
      Validators.min(0)
    ]),
    userLookup: ''
  });

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected organizationService: OrganizationService,
    protected snackBar: MatSnackBar,
    private eventService: EventService,
    private profileService: ProfileService,
    private datePipe: DatePipe
  ) {
    this.profile = this.profileService.profile()!;

    const data = this.route.snapshot.data as {
      event: EventOverview;
    };
    this.event = data.event;

    // Set values for form group
    this.eventForm.patchValue(
      Object.assign({}, this.event, {
        time: this.datePipe.transform(this.event.time, 'yyyy-MM-ddTHH:mm'),
        userLookup: ''
      })
    );

    // Add validator for registration_limit
    this.eventForm.controls['registration_limit'].addValidators(
      Validators.min(this.event.number_registered)
    );

    // Set the organizers
    // If no organizers already, set current user as organizer
    this.organizers = this.isNew()
      ? [this.profile as PublicProfile]
      : this.event.organizers;
  }

  /** Event handler to handle submitting the event form.
   * @returns {void}
   */
  onSubmit() {
    if (this.eventForm.valid) {
      let eventToSubmit = this.event;
      Object.assign(eventToSubmit, this.eventForm.value);
      let id = this.route.snapshot.params['id'];
      console.log(id);
      eventToSubmit.id = id !== 'new' ? id : null;
      eventToSubmit.organization_slug = this.route.snapshot.params['orgid'];
      eventToSubmit.organizers = this.organizers;

      let submittedEvent = this.isNew()
        ? this.eventService.createEvent(eventOverviewToDraft(eventToSubmit))
        : this.eventService.updateEvent(eventOverviewToDraft(eventToSubmit));

      submittedEvent.subscribe({
        next: (event) => this.onSuccess(event),
        error: (err) => this.onError(err)
      });

      this.router.navigate([
        '/organizations/',
        eventToSubmit.organization_slug
      ]);
    }
  }

  /** Event handler to handle resetting the form.
   * @returns {void}
   */
  onReset() {
    this.eventForm.patchValue(
      Object.assign({}, this.event, {
        time: this.datePipe.transform(this.event.time, 'yyyy-MM-ddTHH:mm'),
        userLookup: ''
      })
    );
  }

  /** Event handler to handle deleting the event. */
  onDelete() {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this event?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.eventService.deleteEvent(this.event.id!).subscribe(() => {
        this.router.navigate([`events/`]);
        this.snackBar.open('This event has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }

  /** Takes user back to events page without changing any event info.
   * @returns {void}
   */
  onCancel(): void {
    this.router.navigate([`events/`]);
  }

  /** Opens a confirmation snackbar when an event is successfully created.
   * @returns {void}
   */
  private onSuccess(event: EventOverview): void {
    this.router.navigate(['/events/', event.id]);
    this.snackBar.open(`Event ${this.action()}`, '', { duration: 2000 });
  }

  /** Opens a confirmation snackbar when there is an error creating an event.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open(`Error: Event Not ${this.action()}`, '', {
      duration: 2000
    });
  }

  /** Shorthand for whether an event is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    return this.event.id == null;
  }

  /** Shorthand for determining the action being performed on the event.
   * @returns {string}
   */
  action(): string {
    return this.isNew() ? 'Created' : 'Updated';
  }
}
