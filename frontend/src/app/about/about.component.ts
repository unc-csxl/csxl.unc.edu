import { Component } from '@angular/core';
import { CommunityAgreement } from '../shared/community-agreement/community-agreement.widget';
import { Profile, ProfileService } from '../profile/profile.service';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html'
})
export class AboutComponent {
  public static Route = {
    path: 'about',
    component: AboutComponent
  };

  constructor(
    protected profileService: ProfileService,
    protected dialog: MatDialog
  ) {}

  openAgreementDialog(): void {
    const dialogRef = this.dialog.open(CommunityAgreement, {
      width: '1000px'
      // height: '1000px'
    });
    this.profileService.profile$.subscribe((profile) => {
      if (profile) {
        console.log('profile when opening up view agreement box:', profile);
      }
    });
    dialogRef.afterClosed().subscribe((result) => {
      console.log('Dialog closed with result:', result);
      // Send updated profile to backend after user agrees
    });
  }
}
