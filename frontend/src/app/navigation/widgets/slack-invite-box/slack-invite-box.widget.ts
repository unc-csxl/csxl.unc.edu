import { Component } from '@angular/core';

@Component({
  selector: 'slack-invite-box',
  templateUrl: './slack-invite-box.widget.html',
  styleUrls: ['./slack-invite-box.widget.css']
})
export class SlackInviteBox {
  public realName: boolean = false;
  public profilePicture: boolean = false;
  public communityStandards: boolean = false;
  public fAroundFindOut: boolean = false;

  public get acceptAll(): boolean {
    return (
      this.realName &&
      this.profilePicture &&
      this.communityStandards &&
      this.fAroundFindOut
    );
  }

  constructor() {}

  public openSlackInvite() {
    window.open(
      'https://join.slack.com/t/csxl/shared_invite/zt-1mvfaiqme-fXXw9cKjaXOfhXVBfgXVCA',
      '_blank'
    );
  }
}
