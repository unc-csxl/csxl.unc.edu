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
  TicketDetails,
  TicketState
} from '../../../office-hours.models';
import { OfficeHoursService } from '../../../office-hours.service';
import { RosterRole } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';

@Component({
  selector: 'ticket-history-widget',
  templateUrl: './ticket-history.widget.html',
  styleUrls: ['./ticket-history.widget.css']
})
export class TicketHistoryWidget implements OnInit {
  @Input() sectionId!: number;
  /* Roster role in the course */
  rosterRole: RosterRole | null;
  public createdTickets: Ticket[] = [];
  public calledTickets: TicketDetails[] = [];
  public allSectionTickets: TicketDetails[] = [];
  public displayedStudentColumns: string[] = [
    'date',
    'event-type',
    'TA',
    'description'
  ];
  public displayedCalledColumns: string[] = [
    'date',
    'event-type',
    'student',
    'description',
    'notes',
    'concerns'
  ];
  public displayedAllColumns: string[] = [
    'date',
    'event-type',
    'staff',
    'student',
    'description',
    'notes',
    'concerns'
  ];
  constructor(
    private officeHoursService: OfficeHoursService,
    private academicsService: AcademicsService
  ) {
    this.rosterRole = null;
  }

  ngOnInit(): void {
    this.initializeData();
  }

  initializeData(): void {
    this.checkRosterRole().then(() => {
      // RosterRole is retrieved, so good to go on other actions
      this.getUserTickets();
    });
  }

  checkRosterRole(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.academicsService.getMembershipBySection(this.sectionId).subscribe(
        (section_member) => {
          this.rosterRole = section_member.member_role;
          resolve(); // Resolve the Promise when the roster role is set
        },
        (error) => {
          reject(error); // Reject the Promise if there's an error
        }
      );
    });
  }

  getUserTickets() {
    // Get called tickets + all tickets for anyone other than students
    if (this.rosterRole != RosterRole.STUDENT) {
      this.officeHoursService
        .getUserSectionCalledTickets(this.sectionId)
        .subscribe((tickets) => {
          this.calledTickets = tickets;
        });
      this.officeHoursService
        .getAllSectionTickets(this.sectionId)
        .subscribe((tickets) => {
          this.allSectionTickets = tickets;
        });
    }
    // Populate only created tickets if the user is a student
    else {
      this.officeHoursService
        .getUserSectionCreatedTickets(this.sectionId)
        .subscribe((tickets) => {
          this.createdTickets = tickets;
        });
    }
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

  formatTicketState(typeNum: number) {
    if (typeNum === TicketState.QUEUED) {
      return 'Queued';
    } else if (typeNum === TicketState.CALLED) {
      return 'Called';
    } else if (typeNum === TicketState.CANCELED) {
      return 'Canceled';
    } else if (typeNum === TicketState.CLOSED) {
      return 'Closed';
    } else {
      return 'error';
    }
  }
}
