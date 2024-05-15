/**
 * The Office Hours Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, of } from 'rxjs';
import {
  OfficeHoursSectionDetails,
  OfficeHoursSectionPartial,
  OfficeHoursSectionDraft,
  OfficeHoursEventDetails,
  OfficeHoursEventDraft,
  TicketDetails,
  TicketDraft,
  OfficeHoursEvent,
  OfficeHoursEventType,
  TicketType,
  TicketState,
  TicketPartial,
  Ticket,
  OfficeHoursEventStatus,
  StudentOfficeHoursEventStatus,
  OfficeHoursSection,
  OfficeHoursSectionTrailingData,
  OfficeHoursEventModeType,
  Weekday,
  OfficeHoursEventPartial
} from './office-hours.models';
import {
  Section,
  SectionMember,
  SectionMemberPartial,
  Term
} from '../academics/academics.models';

@Injectable({
  providedIn: 'root'
})
export class OfficeHoursService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  /* Ticket-Related Methods: */

  /** Creates a new ticket
   * @param ticketDraft: Drafted ticket object to create
   * @returns {Observable<TicketDetails>}
   */
  createTicket(ticketDraft: TicketDraft): Observable<TicketDetails> {
    return this.http.post<TicketDetails>(
      '/api/office-hours/ticket',
      ticketDraft
    );
  }

  /** Method that marks a ticket as called by a TA
   * @param ohTicket: Ticket to be called
   * @returns {Observable<TicketDetails>}
   */
  callTicket(ohTicket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/ticket/call',
      ohTicket
    );
  }

  /** Method that marks a ticket as closed
   * @param ohTicket: Ticket to be closed
   * @returns {Observable<TicketDetails>}
   */
  closeTicket(ohTicket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/ticket/close',
      ohTicket
    );
  }

  /** Method which allows students and TAs to cancel tickets
   * @param ohTicket: Ticket to be canceled
   * @returns {Observable<Ticket>}
   */
  cancelTicket(ohTicket: Ticket): Observable<Ticket> {
    return this.http.put<Ticket>('/api/office-hours/ticket/cancel', ohTicket);
  }

  /** Method that fetches a ticket by ID
   * @param ohTicketId: ID of ticket to fetch
   * @returns {Observable<Ticket>}
   */
  getTicket(ohTicketId: number): Observable<Ticket> {
    return this.http.get<Ticket>('/api/office-hours/ticket/' + ohTicketId);
  }

  /** Adds feedback to a closed ticket
   * @param ohTicket: Partial ticket to add feedback to
   * @returns {Observable<TicketDetails>}
   */
  addFeedback(ohTicket: TicketPartial): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/ticket/feedback',
      ohTicket
    );
  }

  /* Ticket Helper Methods: */

  /**
   * Formats TicketType enum value as a string
   * @param typeNum: Numerical representation of TicketType enum value
   * @returns {string}
   */
  formatTicketType(typeNum: number) {
    if (typeNum === TicketType.ASSIGNMENT_HELP) {
      return 'Assignment Help';
    } else return 'Conceptual Help';
  }

  /**
   * Formats TicketState enum value as a string
   * @param stateNum: Numerical representation of TicketState enum value
   * @returns {string}
   */
  formatTicketState(stateNum: number) {
    if (stateNum === TicketState.CALLED) {
      return 'Called';
    } else if (stateNum === TicketState.CANCELED) {
      return 'Canceled';
    } else if (stateNum === TicketState.CLOSED) {
      return 'Closed';
    } else if (stateNum === TicketState.QUEUED) {
      return 'Queued';
    } else {
      return 'error';
    }
  }

  /* Section-Related Methods: */

  /** Creates new Office Hours Section
   * @param sectionDraft: Drafted OH section to create
   * @param academicSectionIds: IDs of academic sections to associate OH section with
   * @returns {Observable<OfficeHoursSectionDetails>}
   */
  createSection(
    sectionDraft: OfficeHoursSectionDraft,
    academicSectionIds: number[]
  ): Observable<OfficeHoursSectionDetails> {
    const requestBody = {
      oh_section: sectionDraft,
      academic_section_ids: academicSectionIds
    };
    return this.http.post<OfficeHoursSectionDetails>(
      '/api/office-hours/section',
      requestBody
    );
  }

  /** Get list of a user's OH Sections in a given term
   * @param termId: Term ID
   * @returns {Observable<OfficeHoursSectionDetails[]>}
   */
  getUserSectionsByTerm(
    termId: string
  ): Observable<OfficeHoursSectionDetails[]> {
    return this.http.get<OfficeHoursSectionDetails[]>(
      '/api/office-hours/section/user/term/' + termId
    );
  }

  /** Get list of OH Sections user hasn't joined in a given term
   * @param termId: Term ID
   * @returns {Observable<OfficeHoursSection[]>}
   */
  getUserSectionsNotEnrolledByTerm(
    termId: string
  ): Observable<OfficeHoursSection[]> {
    return this.http.get<OfficeHoursSection[]>(
      '/api/office-hours/section/user/not-enrolled/term/' + termId
    );
  }

  /** Get list of all OH Sections in a given term
   * @param termId: Term ID
   * @returns {Observable<OfficeHoursSectionDetails[]>}
   */
  getSectionsByTerm(termId: String): Observable<OfficeHoursSectionDetails[]> {
    return this.http.get<OfficeHoursSectionDetails[]>(
      '/api/office-hours/section/term/' + termId
    );
  }

  /** Adds user to OH Section(s)
   * @param ohSections: OH sections to join
   * @returns {Observable<OfficeHoursSection[]>}
   */
  joinSection(ohSections: OfficeHoursSection[]): Observable<SectionMember[]> {
    return this.http.post<SectionMember[]>(
      '/api/academics/section-member',
      ohSections
    );
  }

  /** Get upcoming events for an Office Hours Section within the next week
   * @param ohSectionId: ID of section to get events for
   * @returns {Observable<OfficeHoursEvent[]}
   */
  getUpcomingEventsBySection(
    ohSectionId: number
  ): Observable<OfficeHoursEvent[]> {
    return this.http.get<OfficeHoursEvent[]>(
      'api/office-hours/section/' + ohSectionId + '/events/upcoming'
    );
  }

  /** Get all upcoming events for an Office Hours Section within a semester
   * @param ohSectionId: ID of section to get events for
   * @returns {Observable<OfficeHoursEvent[]>}
   */
  getAllUpcomingEventsBySection(
    ohSectionId: number
  ): Observable<OfficeHoursEvent[]> {
    return this.http.get<OfficeHoursEvent[]>(
      'api/office-hours/section/' + ohSectionId + '/events/upcoming/all'
    );
  }

  /** Get ongoing Office Hours Event for a section
   * @param ohSectionId: ID of section to get events for
   * @returns {Observable<OfficeHoursEvent[]>}
   */
  getCurrentEventsBySection(
    ohSectionId: number
  ): Observable<OfficeHoursEvent[]> {
    return this.http.get<OfficeHoursEvent[]>(
      'api/office-hours/section/' + ohSectionId + '/events/current'
    );
  }

  /** Gets an Office Hours Section by its ID
   * @param ohSectionId: ID of section to get
   * @returns {Observable<OfficeHoursSectionDetails>}
   */
  getSection(ohSectionId: number): Observable<OfficeHoursSectionDetails> {
    return this.http.get<OfficeHoursSectionDetails>(
      'api/office-hours/section/' + ohSectionId
    );
  }

  /** Get all existing tickets for an Office Hours Section
   * @param ohSectionId: ID of section
   * @returns {Observable<TicketDetails[]>}
   */
  getAllSectionTickets(ohSectionId: number): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/section/' + ohSectionId + '/tickets'
    );
  }

  /** Gets tickets created by a user for a given Office Hours Section
   * @param ohSectionId: ID of section
   * @returns {Observable<Ticket[]>}
   */
  getUserSectionCreatedTickets(ohSectionId: number): Observable<Ticket[]> {
    return this.http.get<Ticket[]>(
      'api/office-hours/section/' + ohSectionId + '/user/created_tickets'
    );
  }

  /** Gets tickets called by a user for a given Office Hours Section
   * @param ohSectionId: ID of section
   * @returns {Observable<TicketDetails[]>}
   */
  getUserSectionCalledTickets(
    ohSectionId: number
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/section/' + ohSectionId + '/user/called_tickets'
    );
  }

  /** Gets an Office Hours Section's ticket data for the past week
   * @param ohSectionId: ID of Office Hours section
   * @returns {Observable<OfficeHoursSectionTrailingData>}
   */
  getSectionData(
    ohSectionId: number
  ): Observable<OfficeHoursSectionTrailingData> {
    return this.http.get<OfficeHoursSectionTrailingData>(
      'api/office-hours/section/' + ohSectionId + '/data/statistics'
    );
  }

  /** Gets list of an Office Hours Section's tickets marked for concerns
   * @param ohSectionId: ID of section
   * @returns {Observable<TicketDetails[]>}
   */
  getSectionTicketsWithConcern(
    ohSectionId: number
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/section/' + ohSectionId + '/data/concerns'
    );
  }

  /** Gets list of all members belonging to an Office Hours Section
   * @param ohSectionId: ID of section
   * @returns {Observable<SectionMember[]>}
   */
  getSectionMembers(ohSectionId: number): Observable<SectionMember[]> {
    return this.http.get<SectionMember[]>(
      'api/office-hours/section/' + ohSectionId + '/people'
    );
  }

  /* Event-Related Methods: */

  /** Creates a new Office Hours Event
   * @param eventDraft: draft of Office Hours Event to create
   * @returns {Observable<OfficeHoursEventDetails>}
   */
  createEvent(
    eventDraft: OfficeHoursEventDraft
  ): Observable<OfficeHoursEventDetails> {
    return this.http.post<OfficeHoursEventDetails>(
      '/api/office-hours/event',
      eventDraft
    );
  }

  /** Creates a weekly recurring Office Hours Event
   * @param eventDraft: draft of Office Hours Event to create
   * @param startDate: start date of recurring event
   * @param endDate: end date of recurring event
   * @param selectedDays: days to repeat event on
   * @returns {Observable<OfficeHoursEventDetails>}
   */
  createEventsWeekly(
    eventDraft: OfficeHoursEventDraft,
    startDate: string,
    endDate: string,
    selectedDays: Weekday[]
  ): Observable<OfficeHoursEvent[]> {
    const eventsRequestBody = {
      draft: eventDraft,
      recurring_start_date: startDate,
      recurring_end_date: endDate,
      selected_week_days: selectedDays
    };
    return this.http.post<OfficeHoursEvent[]>(
      '/api/office-hours/event/recurring/weekly/',
      eventsRequestBody
    );
  }

  /** Get list of all tickets belonging to an Office Hours Event
   * @param ohEvent: Office Hours Event to get tickets for
   * @returns {Observable<TicketDetails[]>}
   */
  getEventTickets(
    ohEvent: OfficeHoursEventDetails
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/event/' + ohEvent.id + '/tickets'
    );
  }

  /** Gets list of all currently queued tickets in an Office Hours Event
   * @param ohEvent: Office Hours Event to retrieve queue for
   * @returns {Observable<TicketDetails[]>}
   */
  getEventQueueTickets(
    ohEvent: OfficeHoursEventDetails
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/event/' + ohEvent.id + '/queue'
    );
  }

  /** Gets Office Hours Event by ID
   * @param ohEventId: ID of event
   * @returns {Observable<OfficeHoursEventDetails>}
   */
  getEvent(ohEventId: number): Observable<OfficeHoursEventDetails> {
    return this.http.get<OfficeHoursEventDetails>(
      'api/office-hours/event/' + ohEventId
    );
  }

  /** Updates an Office Hours Event
   * @param ohEvent: Office Hours Event partial to update
   * @returns {Observable<OfficeHoursEventDetails>}
   */
  updateEvent(
    ohEvent: OfficeHoursEventPartial
  ): Observable<OfficeHoursEventDetails> {
    return this.http.put<OfficeHoursEventDetails>(
      'api/office-hours/event',
      ohEvent
    );
  }

  /** Gets counts of Queued and Called Tickets for an event
   * @param ohEventId: ID of Office Hours Event
   * @returns {Observable<OfficeHoursEventStatus>}
   */
  getQueuedAndCalledTicketCount(
    ohEventId: number
  ): Observable<OfficeHoursEventStatus> {
    return this.http.get<OfficeHoursEventStatus>(
      'api/office-hours/event/' + ohEventId + '/queue-stats'
    );
  }

  /** Gets counts of Queued and Called Tickets for an event, as well as user's queue position
   * @param ohEventId: ID of Office Hours Event
   * @param ticketId: user's pending ticket ID
   * @returns {Observable<StudentOfficeHoursEventStatus>}
   */
  getQueueStatsForStudent(
    ohEventId: number,
    ticketId: number
  ): Observable<StudentOfficeHoursEventStatus> {
    return this.http.get<StudentOfficeHoursEventStatus>(
      'api/office-hours/event/' + ohEventId + '/student-queue-stats/' + ticketId
    );
  }

  /** Deletes an Office Hours Event
   * @param id: ID of Office Hours Event
   * @returns {Observable<null>}
   */
  deleteOfficeHoursEvent(id: number) {
    return this.http.delete('api/office-hours/event/' + id);
  }

  /* Event Helper Methods: */

  /**
   * Formats EventType enum value as a string
   * @param typeNum: Numerical representation of EventType enum value
   * @returns {string}
   */
  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else {
      return 'error';
    }
  }

  /**
   * Formats EventModeType enum value as a string
   * @param typeNum: Numerical representation of EventModeType enum value
   * @returns {string}
   */
  formatEventModeType(typeNum: number) {
    if (typeNum === OfficeHoursEventModeType.IN_PERSON) {
      return 'In-Person';
    } else if (typeNum === OfficeHoursEventModeType.VIRTUAL_OUR_LINK) {
      return 'Virtual - Our Link';
    } else if (typeNum === OfficeHoursEventModeType.VIRTUAL_STUDENT_LINK) {
      return 'Virtual - Your Link';
    } else {
      return 'error';
    }
  }

  /* RosterRole-Related Methods: */

  /** Updates role of a user within an Office Hours Section
   * @param userToModify: Section Member partial to update role of
   * @param ohSectionId: ID of Office Hours Section to change role in
   * @returns
   */
  updateMemberRole(
    userToModify: SectionMemberPartial,
    ohSectionId: number
  ): Observable<SectionMember> {
    return this.http.put<SectionMember>(
      'api/office-hours/section/' + ohSectionId + '/update-role',
      userToModify
    );
  }

  /* Roster Role Helper Method: */

  /** Formats RosterRole enum value as a string
   * @param typeNum: Numerical representation of RosterRole enum value
   * @returns {string}
   */
  formatRosterRole(typeNum: number) {
    if (typeNum === 0) {
      return 'Student';
    } else if (typeNum === 1) {
      return 'UTA';
    } else if (typeNum === 2) {
      return 'GTA';
    } else if (typeNum === 3) {
      return 'Instructor';
    } else {
      return 'error';
    }
  }
}
