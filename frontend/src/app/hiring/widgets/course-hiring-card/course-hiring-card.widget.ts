import {
  Component,
  Input,
  OnInit,
  signal,
  WritableSignal
} from '@angular/core';
import {
  ApplicationReviewOverview,
  HiringAssignmentOverview,
  hiringAssignmentOverviewToDraft,
  HiringAssignmentStatus,
  HiringCourseSiteOverview
} from '../../hiring.models';
import { MatDialog } from '@angular/material/dialog';
import { HiringService } from '../../hiring.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'course-hiring-card',
  templateUrl: './course-hiring-card.widget.html',
  styleUrl: './course-hiring-card.widget.css'
})
export class CourseHiringCardWidget implements OnInit {
  @Input() termId!: string;
  @Input() itemInput!: HiringCourseSiteOverview;

  item: WritableSignal<HiringCourseSiteOverview> = signal(this.itemInput);

  /** Store the columns to display in the table */
  public displayedColumns: string[] = [
    'hire',
    'level',
    'position_number',
    'epar',
    'status'
  ];

  constructor(
    protected dialog: MatDialog,
    protected hiringService: HiringService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.item = signal(this.itemInput);
  }

  /** Changes a status for a single assignment. */
  changeAssignmentStatus(
    assignment: HiringAssignmentOverview,
    newStatus: HiringAssignmentStatus
  ) {
    let updatedAssignment = assignment;
    updatedAssignment.status = newStatus;
    let draft = hiringAssignmentOverviewToDraft(
      this.termId,
      this.item(),
      updatedAssignment
    );
    this.hiringService.updateHiringAssignment(draft).subscribe((assignment) => {
      let assignmentIndex = this.item().assignments.findIndex(
        (a) => a.id == assignment.id
      );
      this.item.update((oldItem) => {
        oldItem.assignments[assignmentIndex] = assignment;
        return oldItem;
      });
    });
  }

  deleteAssignment(assignment: HiringAssignmentOverview) {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this assignment?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.hiringService
        .deleteHiringAssignment(assignment.id!)
        .subscribe(() => {
          this.item.update((oldItem) => {
            oldItem.assignments = oldItem.assignments.filter(
              (item) => item.id !== assignment.id
            );
            return oldItem;
          });
          this.snackBar.open('This assignment has been deleted.', '', {
            duration: 2000
          });
        });
    });
  }
}
