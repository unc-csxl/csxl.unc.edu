/** Constructs the Event editor which allows organization members to create events */

import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventSummary, Profile } from 'src/app/models.module';
import { OrgDetailsService } from '../../org-details/org-details.service';
import { profileResolver } from '../../profile/profile.resolver';
import { EventsService } from '../events.service';

@Component({
  selector: 'app-event-editor',
  templateUrl: './event-editor.component.html',
  styleUrls: ['./event-editor.component.css']
})
export class EventEditorComponent {
  public static Route: Route = {
    path: 'organization/:org_id/event/:event_id/edit',
    component: EventEditorComponent,
    title: 'Event Editor',
    resolve: { profile: profileResolver }
  };

  /** Store the event to be edited or created */
  public event: EventSummary;

  /** Store the relevant ids */
  org_id: number = -1;
  event_id: number = -1;

  /** Create a form group */
  public eventForm = this.formBuilder.group({
    name: '',
    time: new Date(),
    location: '',
    description: '',
    public: false
  });

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the user permission value for current organization. */
  public permValue: number = -1;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected orgDetailsService: OrgDetailsService,
    protected snackBar:
      MatSnackBar,
    private eventService: EventsService) {
    /** Add validators to the form */
    const form = this.eventForm;
    form.get('name')?.addValidators(Validators.required);
    form.get('time')?.addValidators(Validators.required);
    form.get('location')?.addValidators(Validators.required);

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    /** Get ids from the url */
    this.route.params.subscribe(params => this.org_id = params["org_id"]);
    this.route.params.subscribe(params => this.event_id = params["event_id"]);

    /** Create the event if the event_id is -1 */
    this.event = {
      id: null,
      name: '',
      time: new Date(),
      location: '',
      description: '',
      org_id: this.org_id,
      public: true,
    };

    /** Retrieve the event with the eventEditorService */
    if (this.event_id != -1) {
      eventService.getEvent(this.event_id).subscribe((event) => this.event = event);
    }
  }

  ngOnInit() {
    // Get currently-logged-in user.
    const data = this.route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    // Load current org ID
    let org_id = this.route.snapshot.params['org_id'];
    this.org_id = org_id;

    // Load current event ID
    let event_id = this.route.snapshot.params['event_id'];
    this.event_id = event_id;

    // Set permission value if profile exists
    if (this.profile) {
      let assocFilter = this.profile.organization_associations.filter((orgRole) => orgRole.org_id == +this.org_id);
      if (assocFilter.length > 0) {
        this.permValue = assocFilter[0].membership_type;
        this.adminPermission = (this.permValue >= 1);
      }
    }

    // If the event exists (id not default -1)
    if (this.event_id != -1) {
      // Get the event and set the form values to the existing event info
      this.eventService.getEvent(this.event_id).subscribe((event) => {
        this.event = event;

        if (event) {
          this.eventForm.setValue({
            name: event.name,
            time: event.time,
            location: event.location,
            description: event.description,
            public: event.public.valueOf()
          });
        }
      });
    }
  }

  /** Event handler to handle submitting the Create Event Form.
   * @returns {void}
  */
  onSubmit = () => {
    if (this.eventForm.valid) {
      Object.assign(this.event, this.eventForm.value)
      if (this.event_id == -1) {
        this.orgDetailsService.create(this.event).subscribe(
          {
            next: (event) => this.onSuccess(event),
            error: (err) => this.onError(err)
          }
        );
      }
      else {
        this.eventService.updateEvent(this.event).subscribe(
          {
            next: (event) => this.onSuccess(event),
            error: (err) => this.onError(err)
          }
        );
      }
      this.router.navigate(['/organization/', this.org_id]);
    }
  }

  /** Opens a confirmation snackbar when an event is successfully created.
   * @returns {void}
  */
  private onSuccess = (event: EventSummary) => {
    this.snackBar.open("Event Edited", "", { duration: 2000 })
  }

  /** Opens a confirmation snackbar when there is an error creating an event.
   * @returns {void}
  */
  private onError = (err: any) => {
    console.error("Event not edited");
  }
}
