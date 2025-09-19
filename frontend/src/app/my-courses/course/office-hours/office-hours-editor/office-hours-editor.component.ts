/**
 * Component that enables the editing of office hours.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, ElementRef, ViewChild } from '@angular/core';
import { courseSitePageGuard } from '../office-hours.guard';
import { officeHoursResolver } from '../office-hours.resolver';
import {
  NewOfficeHours,
  OfficeHours
} from 'src/app/my-courses/my-courses.model';
import { ActivatedRoute, Router } from '@angular/router';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  MyCoursesService,
  Weekday
} from 'src/app/my-courses/my-courses.service';
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

  public days: Record<string, boolean> = {
    [Weekday.Monday]: false,
    [Weekday.Tuesday]: false,
    [Weekday.Wednesday]: false,
    [Weekday.Thursday]: false,
    [Weekday.Friday]: false,
    [Weekday.Saturday]: false,
    [Weekday.Sunday]: false
  };

  public updateRecurrencePattern: boolean = false;

  /** Custom date range validator. */
  dateRangeValidator: ValidatorFn = (
    control: AbstractControl
  ): ValidationErrors | null => {
    const startDateControl = control.get('start_time');
    const endDateControl = control.get('end_time');

    if (
      startDateControl &&
      startDateControl.value &&
      endDateControl &&
      endDateControl.value &&
      startDateControl.value >= endDateControl.value
    ) {
      return { dateRangeInvalid: true };
    }

    return null;
  };

  /** Custom parameterized date range validator. */
  genericDateRangeValidator = (
    startDateLabel: string,
    endDateLabel: string
  ): ValidatorFn => {
    return (control: AbstractControl): ValidationErrors | null => {
      const startDateControl = control.get(startDateLabel);
      const endDateControl = control.get(endDateLabel);

      if (
        startDateControl &&
        startDateControl.value &&
        endDateControl &&
        endDateControl.value &&
        startDateControl.value >= endDateControl.value
      ) {
        if (endDateLabel == 'recur_end') {
          return { recurEndDateInvalid: true };
        } else {
          return { dateRangeInvalid: true };
        }
      }
      return null;
    };
  };

  /** Office Hours Editor Form */
  public officeHoursForm = this.formBuilder.group(
    {
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
    },
    {
      validators: [
        this.genericDateRangeValidator('start_time', 'end_time'),
        this.genericDateRangeValidator('end_time', 'recur_end')
      ]
    }
  );

  @ViewChild('roomInput') input: ElementRef<HTMLInputElement> | undefined;
  public filteredRooms: Room[];

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
    let currentTermEndDate = this.myCoursesService.currentTerms()[0].end;
    let recurrenceEndDate = new Date(
      this.officeHours.recurrence_pattern &&
      this.officeHours.recurrence_pattern.end_date
        ? this.officeHours.recurrence_pattern.end_date
        : currentTermEndDate
    );

    this.officeHoursForm.patchValue(
      Object.assign({}, this.officeHours, {
        start_time: this.datePipe.transform(
          this.officeHours.start_time,
          'yyyy-MM-ddTHH:mm'
        ),
        end_time: this.datePipe.transform(
          this.officeHours.end_time,
          'yyyy-MM-ddTHH:mm'
        ),
        // The truncated date defaults to GMT. When converted to local EST,
        // it rolls the date ~5hrs back to the previous day. Temporary solution
        // is to "add" the extra day back.
        recur_end: this.datePipe.transform(
          new Date(recurrenceEndDate).setDate(recurrenceEndDate.getDate() + 1),
          'yyyy-MM-dd'
        )
      })
    );

    this.days = this.officeHours.recurrence_pattern
      ? {
          [Weekday.Monday]: this.officeHours.recurrence_pattern.recur_monday,
          [Weekday.Tuesday]: this.officeHours.recurrence_pattern.recur_tuesday,
          [Weekday.Wednesday]:
            this.officeHours.recurrence_pattern.recur_wednesday,
          [Weekday.Thursday]:
            this.officeHours.recurrence_pattern.recur_thursday,
          [Weekday.Friday]: this.officeHours.recurrence_pattern.recur_friday,
          [Weekday.Saturday]:
            this.officeHours.recurrence_pattern.recur_saturday,
          [Weekday.Sunday]: this.officeHours.recurrence_pattern.recur_sunday
        }
      : this.days;

    /** Default to disabling recurrence modificatins when updating */
    if (this.officeHours.id !== -1) {
      this.officeHoursForm.controls.recurs.setValue(
        this.officeHours.recurrence_pattern_id !== undefined
      );
      this.officeHoursForm.controls.recurs.disable();
      this.officeHoursForm.controls.recur_end.disable();
    }

    this.filteredRooms = this.rooms;
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

  toggleUpdateRecurrencePattern(checked: boolean): void {
    this.updateRecurrencePattern = checked;
    console.log(this.updateRecurrencePattern);
    this.officeHoursForm.controls.recurs.setValue(
      this.officeHours.recurrence_pattern_id !== undefined
    );
    if (!this.isNew() && checked) {
      this.officeHoursForm.controls.recurs.enable();
      this.officeHoursForm.controls.recur_end.enable();
    } else {
      this.officeHoursForm.controls.recurs.disable();
      this.officeHoursForm.controls.recur_end.disable();
    }
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
      officeHoursToSubmit.start_time = new Date(officeHoursInfo.start_time!);
      officeHoursToSubmit.end_time = new Date(officeHoursInfo.end_time!);

      // Load information from the parent route
      let courseSiteId = +this.route.parent!.snapshot.params['course_site_id'];
      officeHoursToSubmit.course_site_id = courseSiteId;

      let submittedOfficeHours;
      if (recurs || this.updateRecurrencePattern) {
        let recurrencePattern = {
          start_date: new Date(
            new Date(officeHoursToSubmit.start_time).setHours(0, 0, 0, 0)
          ),
          end_date: recur_end
            ? new Date(new Date(recur_end).setHours(0, 0, 0, 0))
            : null,
          recur_monday: this.days[Weekday.Monday],
          recur_tuesday: this.days[Weekday.Tuesday],
          recur_wednesday: this.days[Weekday.Wednesday],
          recur_thursday: this.days[Weekday.Thursday],
          recur_friday: this.days[Weekday.Friday],
          recur_saturday: this.days[Weekday.Saturday],
          recur_sunday: this.days[Weekday.Sunday]
        };
        submittedOfficeHours = this.isNew()
          ? this.myCoursesService.createRecurringOfficeHours(
              courseSiteId,
              officeHoursToSubmit as NewOfficeHours,
              recurrencePattern
            )
          : this.myCoursesService.updateRecurringOfficeHours(
              courseSiteId,
              officeHoursToSubmit,
              recurrencePattern
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
    this.snackBar.open(`${err.error.message}`, '', {
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

  filterRooms() {
    const filterValue = this.input?.nativeElement.value.toLowerCase();
    this.filteredRooms = this.rooms.filter((room) =>
      room.id?.toLowerCase().includes(filterValue?.toLowerCase() || '')
    );
  }
}
