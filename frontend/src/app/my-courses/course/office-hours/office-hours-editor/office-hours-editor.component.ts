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
    room_id: new FormControl('', [Validators.required])
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
      Object.assign(officeHoursToSubmit, this.officeHoursForm.value);

      // Load information from the parent route
      let courseSiteId = +this.route.parent!.snapshot.params['course_site_id'];
      officeHoursToSubmit.course_site_id = courseSiteId;

      let submittedOfficeHours = this.isNew()
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
