/**
 * The Slack Invite Box widget allows CSXL members to join the
 * CSXL Slack as a dialog box. It requires that students fulfill
 * the profile and community standards requirements.
 *
 * @author Rohan Kashyap, Kris Jordan, Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { CommunityAgreement } from 'src/app/shared/community-agreement/community-agreement.widget';

@Component({
  selector: 'slack-invite-box',
  templateUrl: './slack-invite-box.widget.html',
  styleUrls: ['./slack-invite-box.widget.css'],
  standalone: false
})
export class SlackInviteBox {
  public realName: boolean = false;
  public communityStandards: boolean = false;

  public get acceptedAll(): boolean {
    return this.realName && this.communityStandards;
  }

  constructor(
    protected dialogRef: MatDialogRef<SlackInviteBox>,
    protected dialog: MatDialog
  ) {}

  public openAgreementDialog(): void {
    this.dialog.open(CommunityAgreement, {
      width: '1000px',
      maxHeight: '90vh',
      autoFocus: 'dialog'
    });
  }

  public openSlackInvite() {
    window.open(
      'https://join.slack.com/t/csxl/shared_invite/zt-2zco2tt81-JWX7_x8bBa3ZIxRAUFYjnQ',
      '_blank'
    );
  }

  /** Closes the dialog */
  close(): void {
    this.dialogRef.close();
  }
}
