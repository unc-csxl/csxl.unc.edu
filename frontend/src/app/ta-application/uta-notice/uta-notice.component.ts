import { Component, OnInit } from '@angular/core';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'uta-notice',
  templateUrl: './uta-notice.component.html',
  styleUrls: ['./uta-notice.component.css']
})
export class UTANoticeComponent implements OnInit {
  public profile$: Observable<Profile | undefined>;

  constructor(public profileService: ProfileService) {
    this.profile$ = this.profileService.profile$;
  }

  ngOnInit(): void {
    // TODO: Will be implemented once community agreement code is fully approved
    //       in order to check if community agreement has been agreed to by the signed in user.
    throw new Error('Method not implemented.');
  }
}
