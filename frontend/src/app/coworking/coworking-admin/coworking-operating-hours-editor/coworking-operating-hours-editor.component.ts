/**
 * Component that enables the creation of open hours.
 *
 * Referenced office-hours-editor component for implementation.
 *
 * @author David Foss, Ella Gonzales, Tobenna Okoli, Francine Wei
 * @copyright 2024
 * @license MIT
 */
import { Component, effect, Input, WritableSignal } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import {
  OperatingHoursDraft,
  OperatingHours,
  OperatingHoursRecurrenceDraft
} from '../../coworking.models';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CoworkingService } from '../../coworking.service';
import { OperatingHoursCalendar } from 'src/app/shared/operating-hours-calendar/operating-hours-calendar.widget';
import { DatePipe } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { RecurringModifyDialog } from '../recurring-hours-modify-dialog/recurring-hours-modify.dialog';
import { Observable, share } from 'rxjs';
import { RecurringModifyConfirmDialog } from '../recurring-hours-modify-confirm-dialog/recurring-hours-modify-confirm.dialog';
import { ActivatedRoute } from '@angular/router';
import { Term } from 'src/app/academics/academics.models';

@Component({
  selector: 'coworking-operating-hours-editor',
  templateUrl: './coworking-operating-hours-editor.component.html',
  styleUrls: ['./coworking-operating-hours-editor.component.css']
})
export class CoworkingOperatingHoursEditorComponent {
  @Input() operatingHoursSignal!: WritableSignal<OperatingHoursDraft | null>;
  @Input() isPanelVisible!: WritableSignal<boolean>;
  @Input() calendar?: OperatingHoursCalendar;
  public operatingHoursForm: FormGroup;

  constructor(
    protected http: HttpClient,
    private snackBar: MatSnackBar,
    private fb: FormBuilder,
    public coworkingService: CoworkingService,
    protected dialog: MatDialog,
    private route: ActivatedRoute,
    private datePipe: DatePipe
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      currentTerm: Term | undefined;
    };
    this.operatingHoursForm = this.fb.group(
      {
        selected_date: [null, Validators.required],
        start_time: [null, Validators.required],
        end_time: [null, Validators.required],
        recurrence: ['None'],
        recurrence_days: [[]],
        recurrence_end: data.currentTerm?.end
      },
      { validators: [this.dateRangeValidator, this.recurrenceValidator] }
    );

    effect(() => {
      this.operatingHoursForm
        .get('selected_date')
        ?.setValue(this.operatingHoursSignal()?.start);
      this.operatingHoursForm
        .get('start_time')
        ?.setValue(
          this.datePipe.transform(this.operatingHoursSignal()?.start, 'HH:mm')
        );
      this.operatingHoursForm
        .get('end_time')
        ?.setValue(
          this.datePipe.transform(this.operatingHoursSignal()?.end, 'HH:mm')
        );
      this.operatingHoursForm
        .get('recurrence')
        ?.setValue(
          this.operatingHoursSignal()?.recurrence
            ? this.operatingHoursSignal()?.recurrence.recurs_on ==
              parseInt('0011111', 2)
              ? 'Daily'
              : 'Weekly'
            : 'None'
        );
      if (this.operatingHoursSignal()?.recurrence) {
        this.operatingHoursForm.get('recurrence_days')?.setValue(
          ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].filter(
            (_: string, index: number) =>
              (1 << index) &
              (this.operatingHoursSignal()?.recurrence.recurs_on ?? 0) // We do the ?? 0 to cover the impossible event where recurrence is null despite that being checked
          )
        );
        this.operatingHoursForm
          .get('recurrence_end')
          ?.setValue(this.operatingHoursSignal()?.recurrence.end_date);
      }
    });
  }

  /** Custom date range validator. */
  dateRangeValidator: ValidatorFn = (
    control: AbstractControl
  ): ValidationErrors | null => {
    const startTimeControl = control.get('start_time');
    const endTimeControl = control.get('end_time');

    if (
      startTimeControl &&
      startTimeControl.value &&
      endTimeControl &&
      endTimeControl.value &&
      startTimeControl.value >= endTimeControl.value
    ) {
      return { dateRangeInvalid: true };
    }

    return null;
  };

  /** Custom date range validator. */
  recurrenceValidator: ValidatorFn = (
    control: AbstractControl
  ): ValidationErrors | null => {
    const recurrenceControl = control.get('recurrence');
    const recurrenceEndDateControl = control.get('recurrence_end');
    const recurrenceDaysControl = control.get('recurrence_days');

    if (
      recurrenceControl &&
      recurrenceEndDateControl &&
      recurrenceDaysControl &&
      ((recurrenceControl.value != 'None' && !recurrenceEndDateControl.value) ||
        (recurrenceControl.value == 'Weekly' &&
          recurrenceDaysControl.value.length == 0))
    ) {
      return { recurrenceInvalid: true };
    }

    return null;
  };

  onCancel(): void {
    this.operatingHoursForm.reset({
      selected_date: null,
      start_time: null,
      end_time: null,
      recurrence: 'None',
      recurrence_days: [],
      recurrence_end: null
    });

    this.isPanelVisible.set(false);
    this.operatingHoursSignal.set(null);
  }

  /** Delete existing time range. */
  onDelete(): void {
    const id = this.operatingHoursSignal()?.id;

    /** Opens a snackbar if there is an error with getting the id. */
    if (!id) {
      this.snackBar.open(
        'Error: The specified operating hours ID does not exist',
        '',
        {
          duration: 2000
        }
      );
      return;
    }

    if (this.operatingHoursSignal()?.recurrence) {
      this.dialog.open(RecurringModifyDialog, {
        height: '300px',
        width: '300px',
        data: {
          actionName: 'Delete',
          actionFunction: this.doDelete.bind(this, id)
        }
      });
    } else {
      this.doDelete(id);
    }
  }

  doDelete(id: number, cascade: boolean = false): Observable<void> {
    let observable = this.coworkingService
      .deleteOperatingHours(id, cascade)
      .pipe(share());

    /** Opens a confirmation snackbar for successful delete. */
    observable.subscribe({
      next: () => {
        this.snackBar.open('Operating Hours Deleted', '', { duration: 2000 });
        this.calendar?.update();
        this.operatingHoursForm.reset({
          selected_date: null,
          start_time: null,
          end_time: null,
          recurrence: 'None',
          recurrence_days: [],
          recurrence_end: null
        });

        this.isPanelVisible.set(false);
        this.operatingHoursSignal.set(null);
      },
      /** Opens a snackbar for delete error. */
      error: (err) => {
        console.error('Failed to delete operating hours:', err);
        this.snackBar.open('Error: Unable to delete operating hours', '', {
          duration: 2000
        });
      }
    });

    return observable;
  }

  /** Shorthand for whether operating hours is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    return !!!this.operatingHoursSignal()?.id;
  }

  /** Shorthand for determining the action being performed on operating hours.
   * @returns {string}
   */
  action(): string {
    return this.isNew() ? 'Created' : 'Updated';
  }

  /** Event handler to handle submitting the Update Operating Hours Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.operatingHoursForm.valid) {
      let operatingHoursToSubmit = {} as OperatingHoursDraft;

      operatingHoursToSubmit.id = this.operatingHoursSignal()?.id ?? null;

      operatingHoursToSubmit.start = new Date(
        new Date(this.operatingHoursForm.get('selected_date')?.value).setHours(
          this.operatingHoursForm.get('start_time')?.value.split(':')[0],
          this.operatingHoursForm.get('start_time')?.value.split(':')[1]
        )
      );

      operatingHoursToSubmit.end = new Date(
        new Date(this.operatingHoursForm.get('selected_date')?.value).setHours(
          this.operatingHoursForm.get('end_time')?.value.split(':')[0],
          this.operatingHoursForm.get('end_time')?.value.split(':')[1]
        )
      );

      if (this.operatingHoursForm.get('recurrence')?.value != 'None') {
        operatingHoursToSubmit.recurrence = {
          end_date: this.operatingHoursForm.get('recurrence_end')?.value,
          recurs_on:
            this.operatingHoursForm.get('recurrence')?.value == 'Weekly'
              ? this.operatingHoursForm
                  .get('recurrence_days')
                  ?.value.reduce(
                    (acc: number, day: string) =>
                      acc +
                      (1 <<
                        [
                          'Monday',
                          'Tuesday',
                          'Wednesday',
                          'Thursday',
                          'Friday'
                        ].indexOf(day)),
                    0
                  )
              : parseInt('0011111', 2) // Select M-F if daily is picked
        } as OperatingHoursRecurrenceDraft;
      }

      if (
        !this.isNew() &&
        this.operatingHoursSignal()?.recurrence &&
        operatingHoursToSubmit.recurrence &&
        (this.operatingHoursSignal()?.recurrence.end_date !=
          operatingHoursToSubmit.recurrence.end_date ||
          this.operatingHoursSignal()?.recurrence.recurs_on !=
            operatingHoursToSubmit.recurrence.recurs_on)
      ) {
        this.dialog.open(RecurringModifyConfirmDialog, {
          height: '300px',
          width: '300px',
          data: {
            actionName: 'Update',
            actionFunction: this.doSubmit.bind(this, operatingHoursToSubmit)
          }
        });
      } else if (this.operatingHoursSignal()?.recurrence) {
        this.dialog.open(RecurringModifyDialog, {
          height: '300px',
          width: '300px',
          data: {
            actionName: 'Update',
            actionFunction: this.doSubmit.bind(this, operatingHoursToSubmit)
          }
        });
      } else {
        this.doSubmit(operatingHoursToSubmit);
      }
    }
  }

  private doSubmit(
    operatingHours: OperatingHoursDraft,
    cascade: boolean = false
  ): void {
    let submittedOperatingHours = this.isNew()
      ? this.coworkingService.createOperatingHours(operatingHours)
      : this.coworkingService.updateOperatingHours(operatingHours, cascade);

    submittedOperatingHours.subscribe({
      next: (operatingHours) => {
        console.log('SUCCESS');
        this.onSuccess(operatingHours);
      },
      error: (err) => this.onError(err)
    });
  }

  /** Opens a confirmation snackbar when an operating hours is successfully created/updated.
   * @returns {void}
   */
  private onSuccess(operatingHours: OperatingHours): void {
    this.calendar?.update();
    this.snackBar.open(`Operating Hours ${this.action()}`, '', {
      duration: 2000
    });
  }

  /** Opens a snackbar when there is an error updating an operating hours.
   * @returns {void}
   */
  private onError(err: any): void {
    this.snackBar.open(`Error: Operating Hours Not ${this.action()}`, '', {
      duration: 2000
    });
  }
}
