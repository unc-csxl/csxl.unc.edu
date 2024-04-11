import { Component, Input, OnInit } from '@angular/core';
import { OfficeHoursEventType, TicketDetails } from '../../office-hours.models';
import { OfficeHoursService } from '../../office-hours.service';

@Component({
  selector: 'ticket-history-widget',
  templateUrl: './ticket-history.widget.html',
  styleUrls: ['./ticket-history.widget.css']
})
export class TicketHistoryWidget implements OnInit {
  @Input() sectionId!: number;
  public userTickets: TicketDetails[] = [];
  public displayedColumns: string[] = [
    'date',
    'event-type',
    'TA',
    'description'
  ];
  constructor(private officeHoursService: OfficeHoursService) {}

  ngOnInit(): void {
    this.getUserTickets();
  }

  getUserTickets() {
    this.officeHoursService
      .getUserSectionCreatedTickets(this.sectionId)
      .subscribe((tickets) => {
        this.userTickets = tickets;
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
