/**
 * The Coworking Operating Hours Mobile Dialog provides admins
 * with the hours editor form in dialog form, for use on mobile devices.
 *
 * @author David Foss
 * @copyright 2025
 * @license MIT
 */

import { Component, Inject, ViewChild, WritableSignal } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { OperatingHours } from '../../coworking.models';
import { CoworkingOperatingHoursEditorComponent } from '../coworking-operating-hours-editor/coworking-operating-hours-editor.component';
import { OperatingHoursCalendar } from 'src/app/shared/operating-hours-calendar/operating-hours-calendar.widget';

export interface OperatingHoursMobileDialogData {
  selectedOperatingHours: WritableSignal<OperatingHours | null>;
  calendar: OperatingHoursCalendar;
}

@Component({
  selector: 'operating-hours-mobile-dialog',
  templateUrl: './coworking-operating-hours-mobile.dialog.html',
  styleUrls: ['./coworking-operating-hours-mobile.dialog.css']
})
export class OperatingHoursMobileEditorDialog {
  @ViewChild('editor') editor!: CoworkingOperatingHoursEditorComponent;

  constructor(
    protected dialogRef: MatDialogRef<OperatingHoursMobileEditorDialog>,
    @Inject(MAT_DIALOG_DATA) public data: OperatingHoursMobileDialogData
  ) {
    dialogRef.afterClosed().subscribe(() => {
      this.editor.onCancel();
    });
  }

  /** Shorthand for whether operating hours is new or not.
   * @returns {boolean}
   */
  isNew(): boolean {
    // This code is copied from coworking-operating-hours-editor.component.ts
    // We don't simply rely on the editor reference as the editor reference doesn't exist when isNew() is first called
    return !!!this.data.selectedOperatingHours?.()?.id;
  }
}
