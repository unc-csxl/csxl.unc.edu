import { Component, DestroyRef, Inject, signal } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { timer } from 'rxjs';
import { OperatingHours } from '../../coworking.models';
import {
  OperatingHoursService,
  operatingHoursError
} from '../../operating-hours.service';
import {
  newOperatingHoursRange,
  operatingHoursInput
} from '../../operating-hours-time';
import { dateTimeRangeValidator } from '../../../shared/date-time-range/date-time-range.widget';
import { PermissionService } from '../../../permission.service';

export interface OperatingHoursEditorData {
  hours?: OperatingHours;
  schedule: OperatingHours[];
}

@Component({
  selector: 'operating-hours-editor',
  templateUrl: './operating-hours-editor.dialog.html',
  standalone: false
})
export class OperatingHoursEditorDialog {
  saving = signal(false);
  error = signal('');
  form = this.formBuilder.group(
    {
      start: ['', Validators.required],
      end: ['', Validators.required]
    },
    {
      validators: [
        dateTimeRangeValidator('start', 'end'),
        (control) => {
          const { start, end } = control.value;
          if (!start || !end) return null;
          if (
            !this.data.hours &&
            start.slice(0, 10) < operatingHoursInput(new Date()).slice(0, 10)
          )
            return { pastDate: true };
          const conflict = this.data.schedule.some(
            (hours) =>
              hours.id !== this.data.hours?.id &&
              operatingHoursInput(hours.start) <= end &&
              operatingHoursInput(hours.end) >= start
          );
          return conflict ? { overlap: true } : null;
        }
      ]
    }
  );

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: OperatingHoursEditorData,
    private dialogRef: MatDialogRef<OperatingHoursEditorDialog>,
    private formBuilder: FormBuilder,
    private service: OperatingHoursService,
    private permission: PermissionService,
    private snackBar: MatSnackBar,
    destroyRef: DestroyRef
  ) {
    if (data.hours) {
      this.form.setValue({
        start: operatingHoursInput(data.hours.start),
        end: operatingHoursInput(data.hours.end)
      });
    } else {
      this.form.setValue(newOperatingHoursRange(data.schedule));
    }
    timer(0, 1000)
      .pipe(takeUntilDestroyed(destroyRef))
      .subscribe(() => this.form.updateValueAndValidity());
  }

  save(): void {
    this.form.updateValueAndValidity();
    if (this.saving() || this.form.invalid) return;
    const hours = this.data.hours;
    const action = hours ? 'update' : 'create';
    const resource =
      'coworking/operating_hours' + (hours ? `/${hours.id}` : '');
    if (
      !this.permission.checkSignal(
        `coworking.operating_hours.${action}`,
        resource
      )
    ) {
      this.error.set('You do not have permission to change these hours.');
      return;
    }
    const value = this.form.getRawValue();
    const range = { start: value.start!, end: value.end! };
    this.saving.set(true);
    this.error.set('');
    const request = hours
      ? this.service.update(hours.id, range)
      : this.service.create(range);
    request.subscribe({
      next: () => {
        this.snackBar.open('Operating hours saved.', 'Dismiss', {
          duration: 4000
        });
        this.dialogRef.close(true);
      },
      error: (error) => {
        this.saving.set(false);
        this.error.set(operatingHoursError(error));
      }
    });
  }
}
