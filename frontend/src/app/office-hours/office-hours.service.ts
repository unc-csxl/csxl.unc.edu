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
  OfficeHoursSectionTrailingWeekData,
  OfficeHoursEventModeType
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

  createTicket(ticket_draft: TicketDraft): Observable<TicketDetails> {
    return this.http.post<TicketDetails>(
      '/api/office-hours/ticket',
      ticket_draft
    );
  }

  createSection(
    section_draft: OfficeHoursSectionDraft,
    academic_ids: number[]
  ): Observable<OfficeHoursSectionDetails> {
    const requestBody = {
      oh_section: section_draft,
      academic_ids: academic_ids
    };
    return this.http.post<OfficeHoursSectionDetails>(
      '/api/office-hours/section',
      requestBody
    );
  }

  getUserSectionsByTerm(
    term_id: string
  ): Observable<OfficeHoursSectionDetails[]> {
    return this.http.get<OfficeHoursSectionDetails[]>(
      '/api/office-hours/section/user/term/' + term_id
    );
  }

  getUserSectionsNotEnrolledByTerm(
    term_id: string
  ): Observable<OfficeHoursSection[]> {
    return this.http.get<OfficeHoursSection[]>(
      '/api/office-hours/section/user/not-enrolled/term/' + term_id
    );
  }

  getSectionsByTerm(term_id: String): Observable<OfficeHoursSectionDetails[]> {
    return this.http.get<OfficeHoursSectionDetails[]>(
      '/api/office-hours/section/term/' + term_id
    );
  }

  joinSection(oh_sections: OfficeHoursSection[]): Observable<SectionMember[]> {
    return this.http.post<SectionMember[]>(
      '/api/academics/section-member',
      oh_sections
    );
  }

  createEvent(
    event_draft: OfficeHoursEventDraft
  ): Observable<OfficeHoursEventDetails> {
    return this.http.post<OfficeHoursEventDetails>(
      '/api/office-hours/event',
      event_draft
    );
  }

  getEventTickets(
    oh_event: OfficeHoursEventDetails
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/event/' + oh_event.id + '/tickets'
    );
  }

  getEventQueueTickets(
    oh_event: OfficeHoursEventDetails
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/event/' + oh_event.id + '/queue'
    );
  }

  getUpcomingEventsBySection(
    oh_section_id: number
  ): Observable<OfficeHoursEvent[]> {
    return this.http.get<OfficeHoursEvent[]>(
      'api/office-hours/section/' + oh_section_id + '/events/upcoming'
    );
  }

  getCurrentEventsBySection(
    oh_section_id: number
  ): Observable<OfficeHoursEvent[]> {
    return this.http.get<OfficeHoursEvent[]>(
      'api/office-hours/section/' + oh_section_id + '/events/current'
    );
  }

  getEvent(oh_event_id: number): Observable<OfficeHoursEventDetails> {
    return this.http.get<OfficeHoursEventDetails>(
      'api/office-hours/event/' + oh_event_id
    );
  }

  getSection(oh_section_id: number): Observable<OfficeHoursSectionDetails> {
    return this.http.get<OfficeHoursSectionDetails>(
      'api/office-hours/section/' + oh_section_id
    );
  }

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

  formatEventModeType(typeNum: number) {
    if (typeNum === OfficeHoursEventModeType.IN_PERSON) {
      return 'In-Person';
    } else if (typeNum === OfficeHoursEventModeType.VIRTUAL_OUR_LINK) {
      return 'Virtual - Our Link';
    } else if (typeNum === OfficeHoursEventModeType.VIRTUAL_YOUR_LINK) {
      return 'Vritual - Your Link';
    } else {
      return 'error';
    }
  }

  formatTicketType(typeNum: number) {
    if (typeNum === TicketType.ASSIGNMENT_HELP) {
      return 'Assignment Help';
    } else return 'Conceptual Help';
  }

  formatTicketState(typeNum: number) {
    if (typeNum === TicketState.CALLED) {
      return 'Called';
    } else if (typeNum === TicketState.CANCELED) {
      return 'Canceled';
    } else if (typeNum === TicketState.CLOSED) {
      return 'Closed';
    } else if (typeNum === TicketState.QUEUED) {
      return 'Queued';
    } else {
      return 'error';
    }
  }

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

  // id
  callTicket(oh_ticket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/ticket/call',
      oh_ticket
    );
  }

  // id
  closeTicket(oh_ticket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/ticket/close',
      oh_ticket
    );
  }

  // id
  cancelTicket(oh_ticket: Ticket): Observable<Ticket> {
    return this.http.put<Ticket>('/api/office-hours/ticket/cancel', oh_ticket);
  }

  // id, have_concerns, caller_notes
  addFeedback(oh_ticket: TicketPartial): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/ticket/feedback',
      oh_ticket
    );
  }

  getTicket(oh_ticket_id: number): Observable<Ticket> {
    return this.http.get<Ticket>('/api/office-hours/ticket/' + oh_ticket_id);
  }

  getUserSectionCreatedTickets(oh_section_id: number): Observable<Ticket[]> {
    return this.http.get<Ticket[]>(
      'api/office-hours/section/' + oh_section_id + '/user/created_tickets'
    );
  }

  getUserSectionCalledTickets(
    oh_section_id: number
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/section/' + oh_section_id + '/user/called_tickets'
    );
  }

  getQueuedAndCalledTicketCount(
    oh_event_id: number
  ): Observable<OfficeHoursEventStatus> {
    return this.http.get<OfficeHoursEventStatus>(
      'api/office-hours/event/' + oh_event_id + '/queue-stats'
    );
  }

  getQueueStatsForStudent(
    oh_event_id: number,
    ticket_id: number
  ): Observable<StudentOfficeHoursEventStatus> {
    return this.http.get<StudentOfficeHoursEventStatus>(
      'api/office-hours/event/' +
        oh_event_id +
        '/student-queue-stats/' +
        ticket_id
    );
  }

  getSectionData(
    oh_section_id: number
  ): Observable<OfficeHoursSectionTrailingWeekData> {
    return this.http.get<OfficeHoursSectionTrailingWeekData>(
      'api/office-hours/section/' + oh_section_id + '/data/statistics'
    );
  }

  getSectionTicketsWithConcern(
    oh_section_id: number
  ): Observable<TicketDetails[]> {
    return this.http.get<TicketDetails[]>(
      'api/office-hours/section/' + oh_section_id + '/data/concerns'
    );
  }

  getSectionMembers(oh_section_id: number): Observable<SectionMember[]> {
    return this.http.get<SectionMember[]>(
      'api/office-hours/section/' + oh_section_id + '/people'
    );
  }

  updateMemberRole(
    user_to_modify: SectionMemberPartial,
    oh_section_id: number
  ): Observable<SectionMember> {
    return this.http.put<SectionMember>(
      'api/office-hours/section/' + oh_section_id + '/update-role',
      user_to_modify
    );
  }

  deleteOfficeHoursEvent(id: number) {
    return this.http.delete('api/office-hours/event/' + id);
  }
}
