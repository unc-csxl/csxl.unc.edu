/**
 * The Event Calendar Widget displays provided calendar events
 * in a visual and easy to digest way to users
 *
 * @author David Foss
 * @copyright 2024 - 2025
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
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CalendarEvent } from 'src/app/calendar-event';

@Component({
  selector: 'calendar',
  templateUrl: './calendar.widget.html',
  styleUrls: ['./calendar.widget.css']
})
export class Calendar<T extends CalendarEvent> {
  @Input() selectedEvent?: T | null;
  @Input() selectEvent?: (calendar_event: T) => void;
  @Input() getCalendarEvents!: (start: Date, end: Date) => Observable<T[]>;
  protected startDate: WritableSignal<Date>;

  // endDate is midnight on Saturday of the week
  // This should not be used when requesting events as it would miss anything on Saturday
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
  protected calendarEvents: WritableSignal<T[]>;
  protected earliestDay: Signal<number> = computed(() =>
    Math.min(
      1,
      ...this.calendarEvents().map((calendarEvent: T) =>
        calendarEvent.start.getDay()
      )
    )
  );
  protected latestDay: Signal<number> = computed(() =>
    Math.max(
      5,
      ...this.calendarEvents().map((calendarEvent: T) =>
        calendarEvent.end.getDay()
      )
    )
  );
  protected earliestHour: Signal<number> = computed(() =>
    Math.min(
      8,
      ...this.calendarEvents().map((calendarEvent: T) =>
        calendarEvent.start.getHours()
      )
    )
  );
  protected latestHour: Signal<number> = computed(() =>
    Math.max(
      22,
      ...this.calendarEvents().map((calendarEvent: T) =>
        calendarEvent.end.getHours()
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
    this.calendarEvents = signal<T[]>([]);
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
    this.getCalendarEvents(this.startDate(), endDate).subscribe((hours) => {
      this.calendarEvents.set(hours);
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

  /** Processes the click of a given Calendar Event
   *
   * Used to select Calendar Events, if that is an option
   *
   * @param {T} calendarEvent - The Calendar Event that was clicked on
   *
   * @returns {void}
   */
  clickCalendarEvent(calendarEvent: T): void {
    if (this.selectEvent) {
      this.selectEvent(calendarEvent);
    }
  }
}
