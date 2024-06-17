/**
 * The My Courses Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Injectable, WritableSignal, computed, signal } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  OfficeHourEventOverview,
  OfficeHourEventOverviewJson,
  OfficeHourEventRoleOverview,
  OfficeHourQueueOverview,
  OfficeHourQueueOverviewJson,
  OfficeHourTicketOverview,
  OfficeHourTicketOverviewJson,
  TermOverview,
  TermOverviewJson,
  parseOfficeHourEventOverviewJson,
  parseOfficeHourEventOverviewJsonList,
  parseOfficeHourQueueOverview,
  parseOfficeHourTicketOverviewJson,
  parseTermOverviewJsonList
} from './my-courses.model';
import { Observable, map, tap } from 'rxjs';
import { Paginator } from '../pagination';

@Injectable({
  providedIn: 'root'
})
export class MyCoursesService {
  /** Encapsulated terms signal */
  private termsSignal: WritableSignal<TermOverview[]> = signal([]);

  /** Exposed computed signals based on date */
  currentTerms = computed(() => {
    return this.termsSignal().filter((term) => {
      let currentDate = new Date();
      return term.start <= currentDate && currentDate <= term.end;
    });
  });

  pastTerms = computed(() => {
    return this.termsSignal().filter((term) => {
      let currentDate = new Date();
      return term.end < currentDate;
    });
  });

  /** Constructor */
  constructor(
    protected http: HttpClient,
    protected snackBar: MatSnackBar
  ) {
    this.getTermOverviews();
  }

  /** Refreshes the my courses data emitted by the signals. */
  getTermOverviews() {
    this.http
      .get<TermOverviewJson[]>('/api/academics/my-courses')
      .pipe(map(parseTermOverviewJsonList))
      .subscribe((terms) => {
        this.termsSignal.set(terms);
      });
  }

  /**
   * Returns the current and upcoming office hour events for a given course.
   *
   * @param termId: ID for the term of the course
   * @param courseId: ID for the course
   * @returns { Observable<OfficeHourEventOverview[]> }
   */
  getCurrentOfficeHourEvents(
    termId: string,
    courseId: string
  ): Observable<OfficeHourEventOverview[]> {
    return this.http
      .get<OfficeHourEventOverviewJson[]>(
        `/api/academics/my-courses/${termId}/${courseId}/oh-events/current`
      )
      .pipe(map(parseOfficeHourEventOverviewJsonList));
  }

  /**
   * Returns the queue for a given office hours event.
   *
   * @param officeHoursEventId: ID of the office hours event to get the queue for
   * @returns { Observable<OfficeHourQueueOverview> }
   */
  getOfficeHoursQueue(
    officeHoursEventId: number
  ): Observable<OfficeHourQueueOverview> {
    return this.http
      .get<OfficeHourQueueOverviewJson>(
        `/api/academics/my-courses/oh-events/${officeHoursEventId}/queue`
      )
      .pipe(map(parseOfficeHourQueueOverview));
  }

  /**
   * Calls a ticket.
   * @param ticketId: ID of the ticket to call
   * @returns { Observable<OfficeHourTicketOverview> }
   */
  callTicket(ticketId: number): Observable<OfficeHourTicketOverview> {
    return this.http
      .put<OfficeHourTicketOverviewJson>(
        `/api/academics/my-courses/oh-events/ticket/${ticketId}/call`,
        {}
      )
      .pipe(map(parseOfficeHourTicketOverviewJson));
  }

  /**
   * Cancel a ticket.
   * @param ticketId: ID of the ticket to cancel
   * @returns { Observable<OfficeHourTicketOverview> }
   */
  cancelTicket(ticketId: number): Observable<OfficeHourTicketOverview> {
    return this.http
      .put<OfficeHourTicketOverviewJson>(
        `/api/academics/my-courses/oh-events/ticket/${ticketId}/cancel`,
        {}
      )
      .pipe(map(parseOfficeHourTicketOverviewJson));
  }

  /**
   * Close a ticket.
   * @param ticketId: ID of the ticket to close
   * @returns { Observable<OfficeHourTicketOverview> }
   */
  closeTicket(ticketId: number): Observable<OfficeHourTicketOverview> {
    return this.http
      .put<OfficeHourTicketOverviewJson>(
        `/api/academics/my-courses/oh-events/ticket/${ticketId}/close`,
        {}
      )
      .pipe(map(parseOfficeHourTicketOverviewJson));
  }

  /**
   * Returns the role for a given office hours event.
   *
   * @param officeHoursEventId: ID of the office hours event to get the queue for
   * @returns { Observable<OfficeHourEventRoleOverview> }
   */
  getOfficeHoursRole(
    officeHoursEventId: number
  ): Observable<OfficeHourEventRoleOverview> {
    return this.http.get<OfficeHourEventRoleOverview>(
      `/api/academics/my-courses/oh-events/${officeHoursEventId}/role`
    );
  }
}
