import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { UTANoticeComponent } from './uta-notice/uta-notice.component';

@Component({
  selector: 'app-ta-application',
  templateUrl: './ta-application.component.html'
})
export class ApplicationComponent {
  public static Route = {
    path: 'ta-application',
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
