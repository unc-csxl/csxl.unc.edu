/**
 * The Office Hours Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, of } from 'rxjs';
import { TicketDetails, TicketDraft } from './office-hours.models';

@Injectable({
  providedIn: 'root'
})
export class OfficeHoursService {
  private current_ticket: TicketDetails | null;

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {
    this.current_ticket = null;
  }

  createTicket(ticket_draft: TicketDraft): Observable<TicketDetails> {
    return this.http.post<TicketDetails>(
      '/api/office-hours/ticket',
      ticket_draft
    );
  }

  setCurrentTicket(id: Number) {
    this.getTicketById(id).subscribe({
      next: (ticket) => (this.current_ticket = ticket)
    });
  }

  getTicketById(id: Number) {
    return this.http.get<TicketDetails>('/api/office-hours/ticket/' + id);
  }

  getCurrentTicket() {
    return this.current_ticket;
  }
}
