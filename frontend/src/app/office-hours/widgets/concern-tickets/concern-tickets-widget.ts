/**
 * The Concern Tickets widget abstracts the implementation of getting
 * a section's tickets with concern away from other components
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursService } from '../../office-hours.service';
import { OfficeHoursEventType, TicketDetails } from '../../office-hours.models';
import { RosterRole } from 'src/app/academics/academics.models';

@Component({
  selector: 'concern-tickets-widget',
  templateUrl: './concern-tickets-widget.html',
  styleUrls: ['./concern-tickets-widget.css']
})
export class ConcernTicketsWidget implements OnInit {
  @Input() sectionId!: number;
  tickets: TicketDetails[] = [];
  public displayedColumns: string[] = [
    'date',
    'event-type',
    'staff',
    'student',
    'description',
    'notes',
    'concerns'
  ];

  constructor(private officeHoursService: OfficeHoursService) {}

  ngOnInit(): void {
    this.getConcernTickets();
  }

  getConcernTickets() {
    this.officeHoursService
      .getSectionTicketsWithConcern(this.sectionId)
      .subscribe((tickets) => {
        this.tickets = tickets;
      });
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
}
