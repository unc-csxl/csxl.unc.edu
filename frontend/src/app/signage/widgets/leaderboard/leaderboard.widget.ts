/**
 * The Leaderboard Card displays top ten checked in users in a paginated list on the CSXL TV.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { PublicProfile } from 'src/app/profile/profile.service';
import { SignageService } from '../../signage.service';

@Component({
  selector: 'leaderboard',
  templateUrl: './leaderboard.widget.html',
  styleUrls: ['./leaderboard.widget.css']
})
export class LeaderboardWidget implements OnInit {
  /** Inputs and outputs go here */
  @Input() profiles!: PublicProfile[];
  top_five: PublicProfile[] = [];
  lower_five: PublicProfile[] = [];
  @Input() profile!: PublicProfile;

  /** Constructor */
  constructor(public signageService: SignageService) {
    console.log(
      'this is the profiles: ' + this.signageService.slowData().top_users
    );
    console.log(
      'this is the top_five: ' + this.signageService.slowData().top_users
    );
    this.top_five = this.signageService.slowData().top_users.slice(5);
    // this.lower_five = this.profiles.slice(6, 10);
    // console.log(this.top_five);
  }

  ngOnInit(): void {
    console.log(
      'this is the profiles: ' + this.signageService.slowData().top_users
    );
    console.log(
      'this is the top_five: ' + this.signageService.slowData().top_users
    );
  }
}
