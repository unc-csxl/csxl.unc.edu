/**
 * The Operating Hours Dialog Widget provides a space
 * to display the operating hours calendar in any page
 *
 * @author Ajay Gandecha, David Foss
 * @copyright 2024
 * @license MIT
 */

import { Component, signal, WritableSignal } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'operating-hours-dialog',
  templateUrl: './operating-hours-dialog.widget.html',
  styleUrls: ['./operating-hours-dialog.widget.css']
})
export class OperatingHoursDialog {
  constructor(public dialogRef: MatDialogRef<OperatingHoursDialog>) {}
}
