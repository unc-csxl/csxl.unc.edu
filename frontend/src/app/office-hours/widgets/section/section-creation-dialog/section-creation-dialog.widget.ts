/**
 * Section Creation Dialog
 *
 * @author Sadie Amato, Madelyn Andrews, Bailey DeSouza, Meghan Sun
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'section-creation-dialog',
  templateUrl: './section-creation-dialog.widget.html',
  styleUrls: ['./section-creation-dialog.widget.css']
})
export class SectionCreationDialog {
  constructor(public dialogRef: MatDialogRef<SectionCreationDialog>) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}
