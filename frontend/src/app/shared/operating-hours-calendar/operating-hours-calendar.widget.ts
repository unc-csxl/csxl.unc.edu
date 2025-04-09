/**
 * The Operating Hours Calendar Widget displays the current operating hours
 * in a visual and easy to digest way to users
 *
 * @author David Foss
 * @copyright 2024
 * @license MIT
 */

import {
  Component,
  computed,
  effect,
  Input,
  Signal,
  signal,
  WritableSignal
} from '@angular/core';
import {
  OperatingHours,
  OperatingHoursJSON,
  parseOperatingHoursJSONArray
} from 'src/app/coworking/coworking.models';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs';

@Component({
  selector: 'operating-hours-calendar',
  templateUrl: './operating-hours-calendar.widget.html',
  styleUrls: ['./operating-hours-calendar.widget.css']
})
export class OperatingHoursCalendar {
  @Input() selectedOperatingHours?: OperatingHours | null;
  @Input() selectOperatingHours?: (operating_hours: OperatingHours) => void;
  protected startDate: WritableSignal<Date>;

  // endDate is midnight on Saturday of the week
  // This should not be used when requesting operating hours as it would miss anything on Saturday
  protected dates: Signal<Date[]> = computed(() => {
    let newDates: Date[] = [];
    for (let i = 0; i < 7; i++) {
      let newDate = new Date(this.startDate());
      newDate.setDate(this.startDate().getDate() + i);
      newDates.push(newDate);
    }

    return newDates;
  });
  protected currentDate: Signal<Date> = signal(new Date());
  protected operatingHours: WritableSignal<OperatingHours[]>;
  protected earliestDay: Signal<number> = computed(() =>
    Math.min(
      1,
      ...this.operatingHours().map((operatingHour: OperatingHours) =>
        operatingHour.start.getDay()
      )
    )
  );
  protected latestDay: Signal<number> = computed(() =>
    Math.max(
      5,
      ...this.operatingHours().map((operatingHour: OperatingHours) =>
        operatingHour.end.getDay()
      )
    )
  );
  protected earliestHour: Signal<number> = computed(() =>
    Math.min(
      8,
      ...this.operatingHours().map((operatingHour: OperatingHours) =>
        operatingHour.start.getHours()
      )
    )
  );
  protected latestHour: Signal<number> = computed(() =>
    Math.max(
      22,
      ...this.operatingHours().map((operatingHour: OperatingHours) =>
        operatingHour.end.getHours()
      )
    )
  );
  protected hourLabels: Signal<string[]> = computed(() => {
    return Array.from(
      { length: this.latestHour() - this.earliestHour() + 1 },
      (_, i) =>
        ((i + this.earliestHour()) % 12 == 0
          ? 12
          : (i + this.earliestHour()) % 12) +
        (i + this.earliestHour() >= 12 ? ' PM' : ' AM')
    );
  });

  constructor(protected http: HttpClient) {
    this.operatingHours = signal<OperatingHours[]>([]);
    let now = new Date();

    this.startDate = signal<Date>(
      new Date(
        now.getUTCFullYear(),
        now.getUTCMonth(),
        now.getUTCDate() - now.getUTCDay()
      )
    );
  }

  // TODO: Change this to only display 8am - 10pm unless an hour extends earlier than 8am
  public getHourLabels(): Array<string> {
    // Modification on https://stackoverflow.com/questions/3746725/how-to-create-an-array-containing-1-n
    const hourNumbers = [12, ...Array.from({ length: 11 }, (_, i) => i + 1)];
    return [
      ...hourNumbers.map((num: number): string => num.toString() + ' AM'),
      ...hourNumbers.map((num: number): string => num.toString() + ' PM')
    ];
  }

  getHoursEffect = effect(() => {
    this.update();
  });

  /** Updates the calendar with the latest data from the server
   *
   * @returns {void}
   */
  update(): void {
    let endDate = new Date(this.startDate());
    endDate.setDate(this.startDate().getDate() + 7);
    this.http
      .get<OperatingHoursJSON[]>('/api/coworking/operating_hours', {
        params: {
          start: this.startDate().toISOString(),
          end: endDate.toISOString()
        }
      })
      .pipe(map(parseOperatingHoursJSONArray))
      .subscribe((hours) => {
        this.operatingHours.set(hours);
      });
  }

  /** Navigates to the previous week
   *
   * @returns {void}
   */
  previousWeek(): void {
    let newDate = new Date(this.startDate());
    newDate.setDate(this.startDate().getDate() - 7);
    this.startDate.set(newDate);
  }
  /** Navigates to the next week
   *
   * @returns {void}
   */
  nextWeek(): void {
    let newDate = new Date(this.startDate());
    newDate.setDate(this.startDate().getDate() + 7);
    this.startDate.set(newDate);
  }

  /** Processes the click of a given Operating Hours
   *
   * Used to select Operating Hours, if that is an option
   *
   * @param {OperatingHours} operatingHours - The Operating Hours that was clicked on
   *
   * @returns {void}
   */
  clickOperatingHours(operatingHours: OperatingHours): void {
    if (this.selectOperatingHours) {
      this.selectOperatingHours(operatingHours);
    }
  }
}
