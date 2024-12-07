/**
 * Component that enables the creation of open hours.
 *
 * Referenced office-hours-editor component for implementation.
 *
 * @author David Foss, Ella Gonzales, Tobenna Okoli, Francine Wei
 * @copyright 2024
 * @license MIT
 */
import {
  Component,
  effect,
  Input,
  signal,
  WritableSignal
} from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import { OperatingHoursDraft, OperatingHours } from '../../coworking.models';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CoworkingService } from '../../coworking.service';
import { OperatingHoursCalendar } from 'src/app/shared/operating-hours-calendar/operating-hours-calendar.widget';
import { DatePipe } from '@angular/common';

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
    private datePipe: DatePipe
  ) {
    this.operatingHoursForm = this.fb.group(
      {
        selected_date: [null, Validators.required],
        start_time: [null, Validators.required],
        end_time: [null, Validators.required],
        recurrence: ['None'],
        recurrenceDays: [[]]
      },
      { validators: [this.dateRangeValidator] }
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
              parseInt('1111100', 2)
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

  onCancel(): void {
    this.operatingHoursForm.reset({
      selected_date: null,
      start_time: null,
      end_time: null,
      recurrence: 'None',
      recurrenceDays: []
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
    /** Opens a confirmation snackbar for successful delete. */
    this.coworkingService.deleteOperatingHours(id).subscribe({
      next: () => {
        this.snackBar.open('Operating Hours Deleted', '', { duration: 2000 });
        this.calendar?.update();
        this.onCancel();
      },
      /** Opens a snackbar for delete error. */
      error: (err) => {
        console.error('Failed to delete operating hours:', err);
        this.snackBar.open('Error: Unable to delete operating hours', '', {
          duration: 2000
        });
      }
    });
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
      let operatingHoursToSubmit =
        this.operatingHoursSignal() ?? ({} as OperatingHours);

      operatingHoursToSubmit.start = new Date(
        this.operatingHoursForm
          .get('selected_date')
          ?.value.setHours(
            this.operatingHoursForm.get('start_time')?.value.split(':')[0],
            this.operatingHoursForm.get('start_time')?.value.split(':')[1]
          )
      );

      operatingHoursToSubmit.end = new Date(
        this.operatingHoursForm
          .get('selected_date')
          ?.value.setHours(
            this.operatingHoursForm.get('end_time')?.value.split(':')[0],
            this.operatingHoursForm.get('end_time')?.value.split(':')[1]
          )
      );

      let submittedOperatingHours = this.isNew()
        ? this.coworkingService.createOperatingHours(
            operatingHoursToSubmit as OperatingHoursDraft
          )
        : this.coworkingService.updateOperatingHours(operatingHoursToSubmit);

      submittedOperatingHours.subscribe({
        next: (operatingHours) => {
          console.log('SUCCESS');
          this.onSuccess(operatingHours);
        },
        error: (err) => this.onError(err)
      });
    }
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
