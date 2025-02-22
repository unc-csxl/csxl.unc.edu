/**
 * The Leaderboard Card displays top ten checked in users in a paginated list on the CSXL TV.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { SignageProfile } from '../../signage.model';

@Component({
  selector: 'leaderboard',
  templateUrl: './leaderboard.widget.html',
  styleUrls: ['./leaderboard.widget.css']
})
export class LeaderboardWidget implements OnChanges {
  /** Inputs and outputs go here */
  @Input() profiles: SignageProfile[] = []; // Should be a max of 10 elements
  shownIndices: number[] = [...Array(Math.min(5, this.profiles.length)).keys()];

  ngOnChanges(changes: SimpleChanges): void {
    if (
      changes['profiles'] &&
      !this.shownIndices.includes(5) &&
      this.shownIndices.length < 5
    ) {
      // Only run this if there is less than 5 on the leaderboard right now
      this.shownIndices = [...Array(Math.min(5, this.profiles.length)).keys()];
    }
  }

  switchPage() {
    if (this.shownIndices.includes(1)) {
      // Generates an array of numbers 5 to length of profile
      this.shownIndices = [
        ...Array(Math.min(5, this.profiles.length - 5)).keys()
      ].map((i) => i + 5);
    } else {
      // At this point we can assume that the array is larger than 5 elements
      this.shownIndices = [...Array(5).keys()];
    }
  }
}
