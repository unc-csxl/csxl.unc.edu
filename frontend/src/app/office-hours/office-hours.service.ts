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
  TicketPartial,
  Ticket
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

  // id
  callTicket(oh_ticket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>('/api/office-hours/call', oh_ticket);
  }

  // id
  closeTicket(oh_ticket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>('/api/office-hours/close', oh_ticket);
  }

  // id
  cancelTicket(oh_ticket: Ticket): Observable<TicketDetails> {
    return this.http.put<TicketDetails>('/api/office-hours/cancel', oh_ticket);
  }

  // id, have_concerns, caller_notes
  addFeedback(oh_ticket: TicketPartial): Observable<TicketDetails> {
    return this.http.put<TicketDetails>(
      '/api/office-hours/feedback',
      oh_ticket
    );
  }
}
