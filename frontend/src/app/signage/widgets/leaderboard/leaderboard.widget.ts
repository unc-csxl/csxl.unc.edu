/**
 * The Leaderboard Card displays top ten checked in users in a paginated list on the CSXL TV.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { PublicProfile } from 'src/app/profile/profile.service';
import { SignageService } from '../../signage.service';

@Component({
  selector: 'leaderboard',
  templateUrl: './leaderboard.widget.html',
  styleUrls: ['./leaderboard.widget.css']
})
export class LeaderboardWidget implements OnChanges {
  /** Inputs and outputs go here */
  @Input() profiles: PublicProfile[] = []; // Should be a max of 10 elements
  shown_indicies: number[] = [
    ...Array(Math.min(5, this.profiles.length)).keys()
  ];

  ngOnChanges(changes: SimpleChanges): void {
    if (
      changes['profiles'] &&
      !this.shown_indicies.includes(5) &&
      this.shown_indicies.length < 5
    ) {
      // Only run this if there is less than 5 on the leaderboard right now
      this.shown_indicies = [
        ...Array(Math.min(5, this.profiles.length)).keys()
      ];
    }
  }

  switch_page() {
    if (this.shown_indicies.includes(1)) {
      // Generates an array of numbers 5 to length of profile
      this.shown_indicies = [
        ...Array(Math.min(5, this.profiles.length - 5)).keys()
      ].map((i) => i + 5);
    } else {
      // At this point we can assume that the array is larger than 5 elements
      this.shown_indicies = [...Array(5).keys()];
    }
  }
}
