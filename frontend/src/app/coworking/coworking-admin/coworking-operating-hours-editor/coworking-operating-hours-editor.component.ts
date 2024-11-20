/**
 * Component that enables the creation of open hours.
 *
 * Referenced office-hours-editor component for implementation.
 *
 * @author David Foss, Ella Gonzales, Tobenna Okoli
 * @copyright 2024
 * @license MIT
 */
import { Component, Input, WritableSignal } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators
} from '@angular/forms';
import {
  NewOperatingHours,
  OperatingHours,
  OperatingHoursJSON,
  parseOperatingHoursJSON
} from '../../coworking.models';
import { map, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CoworkingService } from '../../coworking.service';
import { OperatingHoursCalendar } from 'src/app/shared/operating-hours-calendar/operating-hours-calendar.widget';

@Component({
  selector: 'coworking-operating-hours-editor',
  templateUrl: './coworking-operating-hours-editor.component.html',
  styleUrls: ['./coworking-operating-hours-editor.component.css']
})
export class CoworkingOperatingHoursEditorComponent {
  @Input() operatingHours?: OperatingHours;
  @Input() isPanelVisible!: WritableSignal<boolean>;
  @Input() calendar?: OperatingHoursCalendar;
  public operatingHoursForm: FormGroup;

  constructor(
    protected http: HttpClient,
    private snackBar: MatSnackBar,
    private fb: FormBuilder,
    public coworkingService: CoworkingService
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
  }

  /** Shorthand for whether operating hours is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    console.log(this.operatingHours?.id);
    console.log(!!!this.operatingHours?.id);
    return !!!this.operatingHours?.id;
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
    if (this.operatingHoursForm.valid) {
      let operatingHoursToSubmit =
        this.operatingHours ?? ({} as OperatingHours);

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
      console.log(operatingHoursToSubmit);

      let submittedOperatingHours = this.isNew()
        ? this.coworkingService.createOperatingHours(
            operatingHoursToSubmit as NewOperatingHours
          )
        : this.coworkingService.updateOperatingHours(operatingHoursToSubmit);

      submittedOperatingHours.subscribe({
        next: (operatingHours) => this.onSuccess(operatingHours),
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
