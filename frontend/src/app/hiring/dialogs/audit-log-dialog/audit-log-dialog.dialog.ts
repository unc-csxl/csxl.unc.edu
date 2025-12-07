/**
 * @author Christian Lee <chjlee@unc.edu>
 * @copyright 2025
 * @license MIT
 */

import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HiringService } from '../../hiring.service';
import { HiringAssignmentAuditOverview } from '../../hiring.models';
import { Observable } from 'rxjs';

export interface AuditLogDialogData {
  assignmentId: number;
  applicantName: string;
}

@Component({
  selector: 'app-audit-log-dialog',
  templateUrl: './audit-log-dialog.dialog.html',
  styleUrls: ['./audit-log-dialog.dialog.css'],
  standalone: false
})
export class AuditLogDialog implements OnInit {
  history$: Observable<HiringAssignmentAuditOverview[]> | undefined;

  constructor(
    protected dialogRef: MatDialogRef<AuditLogDialog>,
    @Inject(MAT_DIALOG_DATA) public data: AuditLogDialogData,
    private hiringService: HiringService
  ) {}

  ngOnInit() {
    this.history$ = this.hiringService.getAuditHistory(this.data.assignmentId);
  }
}
