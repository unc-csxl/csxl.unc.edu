import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MyCoursesService } from '../../my-courses.service';
import { OfficeHourEventOverview } from '../../my-courses.model';

@Component({
    selector: 'dialog-delete-recurring-event',
    templateUrl: './delete-recurring-event.dialog.html',
    styleUrl: './delete-recurring-event.dialog.css',
    standalone: false
})
export class DeleteRecurringEventDialog {
  /** Delete one vs. delete all */

  deleteAll: boolean = false;

  constructor(
    protected dialogRef: MatDialogRef<DeleteRecurringEventDialog>,
    @Inject(MAT_DIALOG_DATA)
    public data: { siteId: number; officeHours: OfficeHourEventOverview },
    protected myCoursesService: MyCoursesService
  ) {}

  confirm(): void {
    if (this.deleteAll) {
      this.myCoursesService
        .deleteRecurringOfficeHours(this.data.siteId, this.data.officeHours.id)
        .subscribe(() => {
          this.close();
        });
    } else {
      this.myCoursesService
        .deleteOfficeHours(this.data.siteId, this.data.officeHours.id)
        .subscribe(() => {
          this.close();
        });
    }
  }

  close(): void {
    this.dialogRef.close();
  }
}
