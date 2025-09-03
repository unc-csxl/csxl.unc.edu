/**
 * The Operating Hours Calendar Widget displays the current operating hours
 * in a visual and easy to digest way to users
 *
 * @author David Foss
 * @copyright 2024 - 2025
 * @license MIT
 */

import {
  Component,
  computed,
  Input,
  Signal,
  signal,
  ViewChild,
  WritableSignal
} from '@angular/core';
import {
  OperatingHours,
  OperatingHoursJSON,
  parseOperatingHoursJSONArray
} from 'src/app/coworking/coworking.models';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Calendar } from '../calendar/calendar.widget';

@Component({
  selector: 'operating-hours-calendar',
  templateUrl: './operating-hours-calendar.widget.html',
  styleUrls: ['./operating-hours-calendar.widget.css']
})
export class OperatingHoursCalendar {
  @Input() selectedOperatingHours?: OperatingHours | null;
  @Input() selectOperatingHours?: (operating_hours: OperatingHours) => void;
  @ViewChild('calendar') calendar!: Calendar<OperatingHours>;

  constructor(protected http: HttpClient) {}

  /** Gets the operating hours for the provided time frame
   *
   * @param {Date} start - The start of the time frame to get operating hours from
   * @param {Date} end - The end of the time frame to get operating hours from
   *
   * @returns {Observable<OperatingHours[]>} - The operating hours found in the provided time frame
   */
  getOperatingHours(start: Date, end: Date): Observable<OperatingHours[]> {
    let endDate = new Date(start);
    endDate.setDate(start.getDate() + 7);
    return this.http
      .get<OperatingHoursJSON[]>('/api/coworking/operating_hours', {
        params: {
          start: start.toISOString(),
          end: end.toISOString()
        }
      })
      .pipe(map(parseOperatingHoursJSONArray));
  }

  /** Updates the calendar
   *
   *
   * @returns {void}
   */
  update(): void {
    this.calendar.update();
  }
}
