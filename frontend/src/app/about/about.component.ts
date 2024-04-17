import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { SlackInviteBox } from '../navigation/widgets/slack-invite-box/slack-invite-box.widget';
@Component({
  selector: 'app-about',
  templateUrl: './about.component.html'
})
export class AboutComponent {
  public static Route = {
    path: 'about',
    component: AboutComponent
  };

  constructor(protected dialog: MatDialog) {}

  onSlackInviteClick(): void {
    const dialogRef = this.dialog.open(SlackInviteBox, {
      width: '1000px',
      autoFocus: false
    });
    dialogRef.afterClosed().subscribe();
  }
}
