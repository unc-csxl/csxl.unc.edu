import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'community-agreement',
  templateUrl: './community-agreement.widget.html',
  styleUrls: ['./community-agreement.widget.css']
})
export class CommunityAgreement {
  constructor(
    public dialogRef: MatDialogRef<CommunityAgreement>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  onCloseClick(): void {
    this.dialogRef.close();
  }
}
