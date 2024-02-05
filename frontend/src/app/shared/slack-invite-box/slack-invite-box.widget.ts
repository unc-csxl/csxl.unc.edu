import { Component, OnInit } from '@angular/core';
import { Profile, ProfileService } from 'src/app/profile/profile.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'slack-invite-box',
  templateUrl: './slack-invite-box.widget.html',
  styleUrls: ['./slack-invite-box.widget.css']
})
export class SlackInviteBox implements OnInit {
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
