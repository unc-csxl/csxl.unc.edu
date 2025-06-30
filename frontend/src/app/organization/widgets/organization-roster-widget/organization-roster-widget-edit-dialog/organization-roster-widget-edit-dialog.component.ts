import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {
  OrganizationMembership,
  OrganizationMembershipPermissionLevel
} from 'src/app/organization/organization.model';

@Component({
  selector: 'organization-roster-edit-dialog',
  templateUrl: './organization-roster-widget-edit-dialog.component.html',
  styleUrls: ['./organization-roster-widget-edit-dialog.component.css']
})
export class OrganizationRosterEditDialogComponent {
  isAdmin: boolean;
  localTitle: string;
  localPermissionLevel: OrganizationMembershipPermissionLevel;

  constructor(
    public dialogRef: MatDialogRef<OrganizationRosterEditDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public membership: OrganizationMembership
  ) {
    // Initialize local state from selected state
    this.isAdmin =
      membership.selected_permission_level ===
      OrganizationMembershipPermissionLevel.ADMIN;
    this.localTitle = membership.selected_title || '';
    this.localPermissionLevel =
      membership.selected_permission_level ||
      OrganizationMembershipPermissionLevel.MEMBER;
  }
  onAdminChange(isAdmin: boolean) {
    this.localPermissionLevel = isAdmin
      ? OrganizationMembershipPermissionLevel.ADMIN
      : OrganizationMembershipPermissionLevel.MEMBER;
  }

  onCancel() {
    this.dialogRef.close(null);
  }

  /** Stages local updates to be saved by user */
  onConfirm() {
    this.membership.selected_title = this.localTitle;
    this.membership.selected_permission_level = this.localPermissionLevel;

    if (
      !this.membership.selected_title ||
      this.membership.selected_title.trim() === ''
    ) {
      this.membership.selected_title = 'Member';
    }
    this.dialogRef.close(this.membership);
  }
}
