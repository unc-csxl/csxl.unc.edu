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
  OfficeHoursSectionDraft,
  TicketDetails,
  TicketDraft
} from './office-hours.models';

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
}
