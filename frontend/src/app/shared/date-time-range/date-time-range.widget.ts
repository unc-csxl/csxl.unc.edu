import { Component, Input } from '@angular/core';
import { FormControl, ValidatorFn } from '@angular/forms';

/** Shared start/end inputs for the Office Hours and coworking editors. */
@Component({
  selector: 'date-time-range',
  templateUrl: './date-time-range.widget.html',
  standalone: false
})
export class DateTimeRangeWidget {
  @Input({ required: true }) startControl!: FormControl<string | null>;
  @Input({ required: true }) endControl!: FormControl<string | null>;
  @Input() startLabel = 'Start Time';
  @Input() endLabel = 'End Time';
}

/** Validate the ordered local datetime strings produced by datetime-local inputs. */
export const dateTimeRangeValidator =
  (startName: string, endName: string): ValidatorFn =>
  (control) => {
    const start = control.get(startName)?.value;
    const end = control.get(endName)?.value;
    return start && end && start >= end ? { dateRangeInvalid: true } : null;
  };
