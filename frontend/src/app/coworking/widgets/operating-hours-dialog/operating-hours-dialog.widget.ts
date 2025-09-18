import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { OperatingHours } from 'src/app/coworking/coworking.models';

@Component({
    selector: 'operating-hours-dialog',
    templateUrl: './operating-hours-dialog.widget.html',
    styleUrls: ['./operating-hours-dialog.widget.css'],
    standalone: false
})
export class OperatingHoursDialog {
  constructor(
    public dialogRef: MatDialogRef<OperatingHoursDialog>,
    @Inject(MAT_DIALOG_DATA) public operatingHours: OperatingHours[]
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
