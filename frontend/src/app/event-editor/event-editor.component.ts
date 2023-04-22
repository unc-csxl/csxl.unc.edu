/** Constructs the Event editor which allows organization members to create events */

import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EventSummary } from 'src/app/models.module';
import { OrgDetailsService } from '../org-details/org-details.service';

@Component({
  selector: 'app-event-editor',
  templateUrl: './event-editor.component.html',
  styleUrls: ['./event-editor.component.css']
})
export class EventEditorComponent {
  public static Route: Route = {
    path: 'organization/:id/event-editor',
    component: EventEditorComponent, 
    title: 'New Event', 
  };

  public event: EventSummary;
  id: string = '';

  public eventForm = this.formBuilder.group({
    name: '',
    time: new Date(),
    location: '',
    description: ''
  });

  constructor(private route: ActivatedRoute, protected formBuilder: FormBuilder, protected orgDetailsService: OrgDetailsService, protected snackBar: MatSnackBar) {
    const form = this.eventForm;
    form.get('name')?.addValidators(Validators.required);
    form.get('time')?.addValidators(Validators.required);
    form.get('location')?.addValidators(Validators.required);

    this.route.params.subscribe( params => this.id=params["id"]);

    this.event = {
      id: null,
      name:'',
      time:new Date(),
      location: '',
      description: '',
      org_id: Number(this.id),
      public: true,
    };
  }

  ngOnInit(): void {
    let event = this.event;

    this.eventForm.setValue({
      name: event.name,
      time: event.time,
      location: event.location,
      description: event.description
    });
  }

  /** Event handler to handle submitting the Create Event Form.
   * @returns {void}
  */
  onSubmit(): void {
    if (this.eventForm.valid) {
      Object.assign(this.event, this.eventForm.value)
      this.orgDetailsService.create(this.event).subscribe(
        {
          next: (event) => this.onSuccess(event),
          error: (err) => this.onError(err)
        } 
      );
    }
  }

  /** Opens a confirmation snackbar when an event is successfully created.
   * @returns {void}
  */
  private onSuccess(event: EventSummary) {
    this.snackBar.open("Event Added", "", { duration: 2000 })
  }

  /** Opens a confirmation snackbar when there is an error creating an event.
   * @returns {void}
  */
  private onError(err: any) {
    console.error("How to handle this?");
  }
}
