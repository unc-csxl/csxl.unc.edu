import { Component, Input } from '@angular/core';
import { ApplicationReviewOverview } from '../../hiring.models';
import { MatDialog } from '@angular/material/dialog';
import { HiringCourseSiteOverview } from '../../hiring-admin/hiring-admin.component';

@Component({
  selector: 'course-hiring-card',
  templateUrl: './course-hiring-card.widget.html',
  styleUrl: './course-hiring-card.widget.css'
})
export class CourseHiringCardWidget {
  @Input() item!: HiringCourseSiteOverview;

  /** Store the columns to display in the table */
  public displayedColumns: string[] = [
    'hire',
    'level',
    'position_number',
    'epar',
    'status'
  ];

  constructor(protected dialog: MatDialog) {}
}
