/**
 * The Coworking Recurring Hours Modify Dialog provides admins
 * with a prompt to modify all related hours when editing/deleting
 * an operating hours instance that is part of a recurrance.
 *
 * @author David Foss
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject, Input } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators
} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Observable } from 'rxjs';

export interface RecurringModifyDialogData {
  actionName: string;
  actionFunction: (cascade: boolean) => Observable<void>;
}

@Component({
  selector: 'recurring-modify-dialog',
  templateUrl: './recurring-hours-modify.dialog.html',
  styleUrls: ['./recurring-hours-modify.dialog.css']
})
export class RecurringModifyDialog {
  @Input() action!: string;

  recurringEffectForm: FormGroup;
  cascades = new FormControl('false', Validators.required);

  constructor(
    private fb: FormBuilder,
    protected dialogRef: MatDialogRef<RecurringModifyDialog>,
    @Inject(MAT_DIALOG_DATA) public data: RecurringModifyDialogData
  ) {
    this.recurringEffectForm = this.fb.group({
      cascades: this.cascades
    });
  }

  /** Confirms the modification action
   *
   * @returns {void}
   */
  confirm(): void {
    this.data.actionFunction(this.cascades.value == 'true').subscribe({
      next: () => {
        this.close();
      }
    });
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }
}
