/**
 * The Ticket History widget abstracts the implementation of a student's ticket history
 * away from other components
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import {
  OfficeHoursEventType,
  Ticket,
  TicketDetails
} from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';

@Component({
  selector: 'ticket-history-widget',
  templateUrl: './ticket-history.widget.html',
  styleUrls: ['./ticket-history.widget.css']
})
export class TicketHistoryWidget implements OnInit {
  @Input() sectionId!: number;
  public createdTickets: Ticket[] = [];
  public calledTickets: TicketDetails[] = [];
  public displayedStudentColumns: string[] = [
    'date',
    'event-type',
    'TA',
    'description'
  ];
  public displayedUTAColumns: string[] = [
    'date',
    'event-type',
    'student',
    'description',
    'notes',
    'concerns'
  ];
  constructor(private officeHoursService: OfficeHoursService) {}

  ngOnInit(): void {
    this.getUserTickets();
  }

  getUserTickets() {
    this.officeHoursService
      .getUserSectionCreatedTickets(this.sectionId)
      .subscribe((tickets) => {
        this.createdTickets = tickets;
        console.log(tickets);
      });
    this.officeHoursService
      .getUserSectionCalledTickets(this.sectionId)
      .subscribe((tickets) => {
        this.calledTickets = tickets;
        console.log(tickets);
      });
  }

  formatEventType(typeNum: number) {
    if (typeNum === OfficeHoursEventType.OFFICE_HOURS) {
      return 'Office Hours';
    } else if (typeNum === OfficeHoursEventType.TUTORING) {
      return 'Tutoring';
    } else if (typeNum === OfficeHoursEventType.REVIEW_SESSION) {
      return 'Review Session';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_OFFICE_HOURS) {
      return 'Virtual Office Hours';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_TUTORING) {
      return 'Virtual Tutoring';
    } else if (typeNum === OfficeHoursEventType.VIRTUAL_REVIEW_SESSION) {
      return 'Virtual Review Session';
    } else {
      return 'error';
    }
  }
}
