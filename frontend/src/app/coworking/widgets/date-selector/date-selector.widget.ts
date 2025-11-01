/**
 * The date selector widget that abstracts date selection.
 *
 * @author Aarjav Jain, John Schachte
 * @copyright 2023
 * @license MIT
 */

import { Component, EventEmitter, Output } from '@angular/core';
import { MatDatepickerInputEvent } from '@angular/material/datepicker';
import { ReservationTableService } from '../../room-reservation/reservation-table.service';

/**
 * @title Date Selector
 */
@Component({
  selector: 'date-selector',
  templateUrl: './date-selector.widget.html',
  standalone: false
})
export class DateSelector {
  @Output() dateSelected = new EventEmitter<Date>();
  minDate: Date;
  maxDate: Date;

  constructor(private reservationTableService: ReservationTableService) {
    this.minDate = this.reservationTableService.setMinDate();
    this.maxDate = this.reservationTableService.setMaxDate();
  }

  onDateChange(event: MatDatepickerInputEvent<Date>) {
    const selectedDate: string = this.formatDate(event.value!);
    this.reservationTableService.setSelectedDate(selectedDate);
  }

  private formatDate(date: Date): string {
    // Format the date as needed, you might want to use a library like 'date-fns' or 'moment'
    // For simplicity, this example uses the default 'toLocaleDateString' method
    return date.toLocaleDateString(); // Adjust this based on your actual formatting requirements
  }
}
