/**
 * The Office Hour Event widget defines the UI card for
 * an office hour event.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import {
  OfficeHourEventOverview,
  OfficeHourEventRoleOverview
} from '../../../../my-courses.model';
import { MyCoursesService } from 'src/app/my-courses/my-courses.service';
import { Observable, map, of } from 'rxjs';

@Component({
    selector: 'office-hour-event-card',
    templateUrl: './office-hour-event-card.widget.html',
    styleUrls: ['./office-hour-event-card.widget.scss'],
    standalone: false
})
export class OfficeHourEventCardWidget implements OnInit {
  /** The event to show */
  @Input() event!: OfficeHourEventOverview;
  @Input() editRoute: string = '';
  /** Role for the event */
  role$: Observable<string> = of('');

  constructor(protected myCoursesService: MyCoursesService) {}

  ngOnInit(): void {
    this.role$ = this.myCoursesService
      .getOfficeHoursRole(this.event.id)
      .pipe(map((roleData) => roleData.role));
  }
}
