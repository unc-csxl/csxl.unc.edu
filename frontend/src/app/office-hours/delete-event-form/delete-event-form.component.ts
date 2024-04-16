/**
 * The Event Deletion Form allows TAs, GTAs, and Instructors to delete upcoming
 * or current Office Hours Events
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { OfficeHoursEvent } from '../office-hours.models';
import { FormBuilder } from '@angular/forms';
import { OfficeHoursService } from '../office-hours.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'delete-event-form',
  templateUrl: './delete-event-form.component.html',
  styleUrls: ['./delete-event-form.component.css']
})
export class DeleteEventFormComponent {
  @Input() isCurrent!: boolean;
  @Input() events!: OfficeHoursEvent[];
  isDeletable: boolean = true;

  constructor(
    protected formBuilder: FormBuilder,
    private officeHoursService: OfficeHoursService,
    protected snackBar: MatSnackBar
  ) {}

  public deleteEventForm = this.formBuilder.group({
    event: ''
  });

  formatEventType(typeNum: number) {
    return this.officeHoursService.formatEventType(typeNum);
  }

  deleteCurrentEvent() {
    console.log(this.events[0]);
    this.officeHoursService
      .deleteOfficeHoursEvent(this.events[0].id)
      .subscribe({
        next: () => this.onSuccess(),
        error: (err) => this.onError(err)
      });
  }

  deleteUpcomingEvent() {
    if (this.deleteEventForm.value.event) {
      this.officeHoursService
        .deleteOfficeHoursEvent(+this.deleteEventForm.value.event)
        .subscribe({
          next: () => this.onSuccess(),
          error: (err) => this.onError(err)
        });
    }
  }

  private onError(err: HttpErrorResponse): void {
    this.snackBar.open(
      'Ticket Data exists for this event. You are unable to delete this event.',
      '',
      {
        duration: 5000
      }
    );
  }

  private onSuccess(): void {
    this.isDeletable = false;
    this.snackBar.open('Event has been deleted!', '', {
      duration: 4000
    });
  }
}
