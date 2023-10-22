/**
 * The Event Editor Component allows users to edit information
 * about events which are publically displayed on the Events page.
 * 
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventService } from '../event.service';
import { profileResolver } from '../../profile/profile.resolver';
import { Profile } from '../../profile/profile.service';
import { OrganizationService } from '../../organization/organization.service';
import { Observable } from 'rxjs';
import { eventDetailResolver } from '../event.resolver';
import { PermissionService } from 'src/app/permission.service';
import { organizationDetailResolver } from 'src/app/organization/organization.resolver';
import { Organization } from 'src/app/organization/organization.model';
import { Event } from '../event.model';

@Component({
  selector: 'app-event-editor',
  templateUrl: './event-editor.component.html',
  styleUrls: ['./event-editor.component.css']
})
export class EventEditorComponent {
  public static Route: Route = {
    path: 'organizations/:slug/events/:id/edit',
    component: EventEditorComponent,
    title: 'Event Editor',
    resolve: { profile: profileResolver, organization: organizationDetailResolver, event: eventDetailResolver }
  };

  /** Store the event to be edited or created */
  public event: Event;
  public organization_slug: string;
  public organization: Organization;

  public event_id: number = -1;

  public profile: Profile | null = null;

  /** Stores whether the user has admin permission over the current organization. */
  public adminPermission$: Observable<boolean>;

  /** Add validators to the form */
  name = new FormControl('', [Validators.required]);
  time = new FormControl('', [Validators.required]);
  location = new FormControl('', [Validators.required]);
  description = new FormControl('', [Validators.required, Validators.maxLength(2000)]);
  public = new FormControl('', [Validators.required]);

  /** Create a form group */
  public eventForm = this.formBuilder.group({
    name: this.name,
    time: new Date(this.time.value!),
    location: this.location,
    description: this.description,
    public: (this.public.value! == "true")
  });

  constructor(private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected organizationService: OrganizationService,
    protected snackBar: MatSnackBar,
    private eventService: EventService,
    private permission: PermissionService) {

    /** Get currently-logged-in user. */
    const data = route.snapshot.data as { profile: Profile, organization: Organization, event: Event };
    this.profile = data.profile;

    /** Initialize event */
    this.organization = data.organization;
    this.event = data.event;
    this.event.organization_id = this.organization.id;

    /** Get ids from the url */
    let organization_slug = this.route.snapshot.params['slug'];
    this.organization_slug = organization_slug;

    this.eventForm.setValue({
      name: this.event.name,
      time: this.event.time,
      location: this.event.location,
      description: this.event.description,
      public: this.event.public
    })

    /** Set permission value */
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
  }

  /** Event handler to handle submitting the Create Event Form.
   * @returns {void}
  */
  onSubmit = () => {
    if (this.eventForm.valid) {
      Object.assign(this.event, this.eventForm.value)
      if (this.event_id == -1) {
        this.eventService.createEvent(this.event).subscribe(
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
      this.router.navigate(['/organization/', this.organization_slug]);
    }
  }

  /** Opens a confirmation snackbar when an event is successfully created.
   * @returns {void}
  */
  private onSuccess(event: Event): void {
    this.router.navigate(['/events/', event.id]);
    this.snackBar.open("Event Edited", "", { duration: 2000 })
  }

  /** Opens a confirmation snackbar when there is an error creating an event.
   * @returns {void}
  */
  private onError(err: any): void {
    console.error("Error: Event Not Created");
    this.snackBar.open("Error: Event Not Created", "", { duration: 2000 })
  }
}
