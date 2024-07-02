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
  OfficeHourGetHelpOverview,
  OfficeHourGetHelpOverviewJson,
  OfficeHourQueueOverview,
  OfficeHourQueueOverviewJson,
  OfficeHourTicketOverview,
  OfficeHourTicketOverviewJson,
  TermOverview,
  TermOverviewJson,
  parseOfficeHourEventOverviewJson,
  parseOfficeHourEventOverviewJsonList,
  parseOfficeHourGetHelpOverviewJson,
  parseOfficeHourQueueOverview,
  parseOfficeHourTicketOverviewJson,
  parseTermOverviewJsonList,
  TicketDraft,
  NewCourseSite,
  CourseSite,
  OfficeHours,
  OfficeHoursJson,
  parseOfficeHoursJson,
  NewOfficeHours
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
      return currentDate <= term.end;
    });
  });

  pastTerms = computed(() => {
    return this.termsSignal().filter((term) => {
      let currentDate = new Date();
      return term.end < currentDate;
    });
  });

  allTerms = computed(() => {
    return this.termsSignal();
  });

  teachingCoursesWithNoSite = computed(() => {
    return this.termsSignal()
      .flatMap((term) => term.teaching_no_site.length > 0)
      .includes(true);
  });

  courseOverview(id: number) {
    return this.termsSignal()
      .flatMap((term) => term.sites)
      .find((site) => site.id == id);
  }

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
      .get<TermOverviewJson[]>('/api/my-courses')
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
    courseSiteId: string
  ): Observable<OfficeHourEventOverview[]> {
    return this.http
      .get<OfficeHourEventOverviewJson[]>(
        `/api/my-courses/${courseSiteId}/oh-events/current`
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
        `/api/office-hours/${officeHoursEventId}/queue`
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
        `/api/office-hours/ticket/${ticketId}/call`,
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
        `/api/office-hours/ticket/${ticketId}/cancel`,
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
        `/api/office-hours/ticket/${ticketId}/close`,
        {}
      )
      .pipe(map(parseOfficeHourTicketOverviewJson));
  }

  /**
   * Returns the role for a given office hours event.
   *
   * @param officeHoursEventId: ID of the office hours event to get the role for
   * @returns { Observable<OfficeHourEventRoleOverview> }
   */
  getOfficeHoursRole(
    officeHoursEventId: number
  ): Observable<OfficeHourEventRoleOverview> {
    return this.http.get<OfficeHourEventRoleOverview>(
      `/api/office-hours/${officeHoursEventId}/role`
    );
  }

  /**
   * Returns the summary with information for a user's tickets and queue position.
   *
   * @param officeHoursEventId: ID of the office hours event
   * @returns { Observable<OfficeHourGetHelpOverview> }
   */
  getOfficeHoursHelpOverview(
    officeHoursEventId: number
  ): Observable<OfficeHourGetHelpOverview> {
    return this.http
      .get<OfficeHourGetHelpOverviewJson>(
        `/api/office-hours/${officeHoursEventId}/get-help`
      )
      .pipe(map(parseOfficeHourGetHelpOverviewJson));
  }

  /** Creates a new ticket
   * @param ticketDraft: Drafted ticket object to create
   * @returns {Observable<TicketDetails>}
   */
  createTicket(ticketDraft: TicketDraft): Observable<OfficeHourTicketOverview> {
    return this.http.post<OfficeHourTicketOverview>(
      'api/office-hours/ticket/',
      ticketDraft
    );
  }

  /**
   * Creates a new course site.
   * @param newCourseSite New course site to create
   * @returns {Observable<CourseSite>}
   */
  createCourseSite(newCourseSite: NewCourseSite): Observable<CourseSite> {
    return this.http.post<CourseSite>(`/api/my-courses/new`, newCourseSite);
  }

  /**
   * Imports a roster for from a Canvas CSV File
   * @returns {Observable<{ uploaded: number }>}
   */
  importRosterFromCanvasCSV(
    section_id: number,
    csvData: string
  ): Observable<{ uploaded: number }> {
    return this.http.post<{ uploaded: number }>(
      `/api/academics/section-member/import-from-canvas/${section_id}`,
      {
        csv_data: csvData
      }
    );
  }

  /**
   * Retrieve office hours.
   * @param siteId: ID of the site to look for office hours.
   * @param officeHoursId: ID of the office hours.
   * @returns {Observable<OfficeHours>}
   */
  getOfficeHours(
    siteId: number,
    officeHoursId: number
  ): Observable<OfficeHours> {
    return this.http
      .get<OfficeHoursJson>(`/api/office-hours/${siteId}/${officeHoursId}`)
      .pipe(map(parseOfficeHoursJson));
  }

  /**
   * Create office hours.
   * @param siteId: ID of the site to look for office hours.
   * @param officeHours: Office hours object to create.
   * @returns {Observable<OfficeHours>}
   */
  createOfficeHours(
    siteId: number,
    officeHours: NewOfficeHours
  ): Observable<OfficeHours> {
    return this.http
      .post<OfficeHoursJson>(`/api/office-hours/${siteId}`, officeHours)
      .pipe(map(parseOfficeHoursJson));
  }

  /**
   * Update office hours.
   * @param siteId: ID of the site to look for office hours.
   * @param officeHours: Office hours object to update.
   * @returns {Observable<OfficeHours>}
   */
  updateOfficeHours(
    siteId: number,
    officeHours: OfficeHours
  ): Observable<OfficeHours> {
    return this.http
      .put<OfficeHoursJson>(`/api/office-hours/${siteId}`, officeHours)
      .pipe(map(parseOfficeHoursJson));
  }

  /**
   * Delete office hours.
   * @param siteId: ID of the site to look for office hours.
   * @param officeHoursId: ID of the office hours.
   */
  deleteOfficeHours(siteId: number, officeHoursId: number) {
    return this.http.delete(`/api/office-hours/${siteId}/${officeHoursId}`);
  }
}
