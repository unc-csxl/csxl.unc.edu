import {
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  signal,
  WritableSignal
} from '@angular/core';
import {
  ApplicationReviewOverview,
  HiringAdminCourseOverview,
  HiringAssignmentOverview,
  hiringAssignmentOverviewToDraft,
  HiringAssignmentStatus,
  HiringCourseSiteOverview
} from '../../hiring.models';
import { MatDialog } from '@angular/material/dialog';
import { HiringService } from '../../hiring.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  CreateAssignmentDialog,
  CreateAssignmentDialogData
} from '../../dialogs/create-assignment-dialog/create-assignment.dialog';
import { PublicProfile } from 'src/app/profile/profile.service';
import {
  QuickCreateAssignmentDialog,
  QuickCreateAssignmentDialogData
} from '../../dialogs/quick-create-assignment-dialog/quick-create-assignment.dialog';
import {
  EditAssignmentDialog,
  EditAssignmentDialogData
} from '../../dialogs/edit-assignment-dialog/edit-assignment.dialog';
import { ApplicationDialog } from '../../dialogs/application-dialog/application-dialog.dialog';

@Component({
    selector: 'course-hiring-card',
    templateUrl: './course-hiring-card.widget.html',
    styleUrl: './course-hiring-card.widget.css',
    standalone: false
})
export class CourseHiringCardWidget implements OnInit {
  @Input() termId!: string;
  @Input() itemInput!: HiringCourseSiteOverview;
  @Output() updateData = new EventEmitter();

  item: WritableSignal<HiringAdminCourseOverview | null> = signal(null);

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
    this.hiringService
      .getHiringAdminCourseOverview(this.itemInput.course_site_id)
      .subscribe((courseOverview) => {
        this.item.set(courseOverview);
      });
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
      this.itemInput,
      updatedAssignment,
      null
    );
    this.hiringService.updateHiringAssignment(draft).subscribe((assignment) => {
      let assignmentIndex = this.item()!.assignments.findIndex(
        (a) => a.id == assignment.id
      );
      this.item.update((oldItem) => {
        oldItem!.assignments[assignmentIndex] = assignment;
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
          this.updateData.emit();
          this.snackBar.open('This assignment has been deleted.', '', {
            duration: 2000
          });
        });
    });
  }

  createAssignment(): void {
    let dialogRef = this.dialog.open(CreateAssignmentDialog, {
      height: '700px',
      width: '800px',
      data: {
        termId: this.termId,
        courseSite: this.itemInput,
        courseAdmin: this.item()!
      } as CreateAssignmentDialogData
    });
    dialogRef.afterClosed().subscribe((assignment) => {
      if (assignment) {
        this.updateData.emit();
      }
    });
  }

  /** Opens the dialog to create an assignment from a existing instructor preference. */
  quickCreateAssignment(user: PublicProfile): void {
    if (!this.chipSelected(user)) {
      let dialogRef = this.dialog.open(QuickCreateAssignmentDialog, {
        height: '700px',
        width: '800px',
        data: {
          user: user,
          termId: this.termId,
          courseSite: this.itemInput,
          courseAdmin: this.item()!
        } as QuickCreateAssignmentDialogData
      });
      dialogRef.afterClosed().subscribe((assignment) => {
        if (assignment) {
          this.updateData.emit();
        }
      });
    }
  }

  editAssignment(assignment: HiringAssignmentOverview): void {
    let dialogRef = this.dialog.open(EditAssignmentDialog, {
      height: '700px',
      width: '800px',
      data: {
        assignment: assignment,
        termId: this.termId,
        courseSite: this.itemInput,
        courseAdmin: this.item()!
      } as EditAssignmentDialogData
    });
    dialogRef.afterClosed().subscribe((assignment) => {
      if (assignment) {
        this.updateData.emit();
      }
    });
  }

  chipSelected(user: PublicProfile): boolean {
    return (
      this.item()!
        .assignments.map((assignment) => assignment.user)
        .filter((u) => u.id === user.id).length > 0
    );
  }
}
