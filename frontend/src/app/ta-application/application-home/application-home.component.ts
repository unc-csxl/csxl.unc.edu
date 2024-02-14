import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { UTANoticeComponent } from '../uta-notice/uta-notice.component';

@Component({
  selector: 'application-home',
  templateUrl: './application-home.component.html'
})
export class ApplicationComponent {
  public static Route = {
    path: '',
    component: ApplicationComponent
  };

  constructor(protected dialog: MatDialog) {}

  onApplicationClick(): void {
    const dialogRef = this.dialog.open(UTANoticeComponent, {
      width: '1000px',
      autoFocus: false
    });
    dialogRef.afterClosed().subscribe();
  }
}
