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
import { Observable } from 'rxjs';
import {
  OfficeHoursSectionDetails,
  OfficeHoursSectionPartial,
  OfficeHoursSectionDraft,
  OfficeHoursEventDetails,
  OfficeHoursEventDraft,
  TicketDetails,
  TicketDraft,
  OfficeHoursEvent
} from './office-hours.models';
import { SectionMember } from '../academics/academics.models';

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

  getSectionsByTerm(term_id: String): Observable<OfficeHoursSectionDetails[]> {
    return this.http.get<OfficeHoursSectionDetails[]>(
      '/api/office-hours/section/term/' + term_id
    );
  }

  joinSection(
    oh_sections: OfficeHoursSectionDetails[]
  ): Observable<SectionMember[]> {
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
    section_id: number
  ): Observable<OfficeHoursEvent[]> {
    return this.http.get<OfficeHoursEvent[]>(
      'api/office-hours/section/' + section_id + '/events/upcoming'
    );
  }
}
