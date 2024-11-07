/**
 * Component that enables the editing of office hours.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import {
  courseSitePageGuard,
  officeHourPageGuard
} from '../office-hours.guard';
import { officeHoursResolver } from '../office-hours.resolver';
import {
  NewOfficeHours,
  OfficeHours
} from 'src/app/my-courses/my-courses.model';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import { DatePipe } from '@angular/common';
import { roomsResolver } from 'src/app/academics/academics.resolver';
import { Room } from 'src/app/coworking/coworking.models';

@Component({
  selector: 'app-office-hours-editor',
  templateUrl: './office-hours-editor.component.html',
  styleUrl: './office-hours-editor.component.css'
})
export class OfficeHoursEditorComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'office-hours/:event_id/edit',
    title: 'Office Hours Editor',
    component: OfficeHoursEditorComponent,
    canActivate: [courseSitePageGuard(['UTA', 'GTA', 'Instructor'])],
    resolve: {
      officeHours: officeHoursResolver,
      rooms: roomsResolver
    }
  };

  /** Stores the office hours.  */
  public officeHours: OfficeHours;
  /** Stores the rooms. */
  public rooms: Room[];
  /* Holds the virtual room. */
  virtualRoom: Room | undefined;

  public days: { [day: string]: boolean } = {
    Mon: false,
    Tues: false,
    Wed: false,
    Thurs: false,
    Fri: false,
    Sat: false,
    Sun: false
  };

  /** Office Hours Editor Form */
  public officeHoursForm = this.formBuilder.group({
    type: new FormControl(0, [Validators.required]),
    mode: new FormControl(0, [Validators.required]),
    description: new FormControl(''),
    location_description: new FormControl(''),
    start_time: new FormControl(
      this.datePipe.transform(new Date(), 'yyyy-MM-ddTHH:mm'),
      [Validators.required]
    ),
    end_time: new FormControl(
      this.datePipe.transform(new Date(), 'yyyy-MM-ddTHH:mm'),
      [Validators.required]
    ),
    room_id: new FormControl('', [Validators.required]),
    recurs: new FormControl(false, [Validators.required]),
    recur_end: new FormControl(
      this.datePipe.transform(new Date(), 'yyyy-MM-dd'),
      []
    )
  });

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    protected myCoursesService: MyCoursesService,
    private datePipe: DatePipe
  ) {
    const data = this.route.snapshot.data as {
      officeHours: OfficeHours;
      rooms: Room[];
    };
    this.officeHours = data.officeHours;
    this.rooms = data.rooms;
    this.virtualRoom = this.rooms.find((room) => room.id === 'Virtual');

    /** Set form data */
    this.officeHoursForm.patchValue(
      Object.assign({}, this.officeHours, {
        start_time: this.datePipe.transform(
          this.officeHours.start_time,
          'yyyy-MM-ddTHH:mm'
        ),
        end_time: this.datePipe.transform(
          this.officeHours.end_time,
          'yyyy-MM-ddTHH:mm'
        )
      })
    );
  }

  /** "Null" comparator function to prevent keyvalue pipe from sorting
   * the day keys alphabetically.
   */
  maintainOriginalOrder = () => 0;

  /** Toggles day boolean to determine which days should be included in
   * the recurrence.
   */
  toggleDay(day: string) {
    this.days[day] = !this.days[day];
  }

  /** Shorthand for whether office hours is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    return this.officeHours.id === -1;
  }

  /** Shorthand for determining the action being performed on office hours.
   * @returns {string}
   */
  action(): string {
    return this.isNew() ? 'Created' : 'Updated';
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.officeHoursForm.valid) {
      let officeHoursToSubmit = this.officeHours;
      let { recurs, recur_end, ...officeHoursInfo } =
        this.officeHoursForm.value;
      Object.assign(officeHoursToSubmit, officeHoursInfo);

      // Load information from the parent route
      let courseSiteId = +this.route.parent!.snapshot.params['course_site_id'];
      officeHoursToSubmit.course_site_id = courseSiteId;

      let submittedOfficeHours;
      if (recurs) {
        let recurrence = {
          start_date: new Date(
            new Date(officeHoursToSubmit.start_time).setHours(0, 0, 0, 0)
          ),
          end_date: recur_end
            ? new Date(new Date(recur_end).setHours(0, 0, 0, 0))
            : null,
          recur_monday: this.days['Mon'],
          recur_tuesday: this.days['Tues'],
          recur_wednesday: this.days['Wed'],
          recur_thursday: this.days['Thurs'],
          recur_friday: this.days['Fri'],
          recur_saturday: this.days['Sat'],
          recur_sunday: this.days['Sun']
        };
        submittedOfficeHours = this.myCoursesService.createRecurringOfficeHours(
          courseSiteId,
          officeHoursToSubmit as NewOfficeHours,
          recurrence
        );

        submittedOfficeHours.subscribe({
          next: (officeHours) => this.onSuccess(officeHours[0]),
          error: (err) => this.onError(err)
        });
      } else {
        submittedOfficeHours = this.isNew()
          ? this.myCoursesService.createOfficeHours(
              courseSiteId,
              officeHoursToSubmit as NewOfficeHours
            )
          : this.myCoursesService.updateOfficeHours(
              courseSiteId,
              officeHoursToSubmit
            );

        submittedOfficeHours.subscribe({
          next: (officeHours) => this.onSuccess(officeHours),
          error: (err) => this.onError(err)
        });
      }
    }
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
   */
  private onSuccess(officeHours: OfficeHours): void {
    this.router.navigate([
      '/course/',
      officeHours.course_site_id,
      'office-hours'
    ]);
    this.snackBar.open(`Office Hours ${this.action()}`, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating an organization.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open(`Error: Office Hours Not ${this.action()}`, '', {
      duration: 2000
    });
  }

  /** Event handler to handle resetting the form.
   * @returns {void}
   */
  onReset() {
    this.officeHoursForm.patchValue(
      Object.assign({}, this.officeHours, {
        start_time: this.datePipe.transform(
          this.officeHours.start_time,
          'yyyy-MM-ddTHH:mm'
        ),
        end_time: this.datePipe.transform(
          this.officeHours.end_time,
          'yyyy-MM-ddTHH:mm'
        )
      })
    );
  }

  modeChanged() {
    if (this.officeHoursForm.controls['mode'].value === 0) {
      this.officeHoursForm.controls['room_id'].setValue('');
    } else {
      this.officeHoursForm.controls['room_id'].setValue(this.virtualRoom!.id);
    }
  }

  /** The following conversion functions are temporarily needed until we can complete a migration. */
  numberToType(type: number) {
    if (type === 0) return 'Office Hours';
    if (type === 1) return 'Tutoring';
    if (type === 2) return 'Review Session';
    return '';
  }
  numberToMode(mode: number) {
    if (mode === 0) return 'In-Person';
    if (mode === 1) return 'Virtual - Student Link';
    if (mode === 2) return 'Virtual - Our Link';
    return '';
  }
}
