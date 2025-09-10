/**
 * The Leaderboard Card displays top ten checked in users in a paginated list on the CSXL TV.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, effect, input } from '@angular/core';
import { SignageProfile } from '../../signage.model';

@Component({
    selector: 'leaderboard',
    templateUrl: './leaderboard.widget.html',
    styleUrls: ['./leaderboard.widget.css'],
    standalone: false
})
export class LeaderboardWidget {
  profiles = input<SignageProfile[]>([]); // This array should have at most 10 elements
  shownIndices: number[] = [
    ...Array(Math.min(5, this.profiles().length)).keys()
  ]; // Stores what indicies of profiles we should show in array. Defaults to 1..min(5, profiles.length)

  constructor() {
    effect(() => {
      /**
       * When we get new profiles from the backend, and the page spinner isn't running yet (we have less than 5 shown rn),
       * then we need to update the shown indicies to include the new amount.
       */
      if (!this.shownIndices.includes(5) && this.shownIndices.length < 5) {
        // Set shownIndicies to length of profiles if there is less than 5 on the leaderboard right now
        this.shownIndices = [
          ...Array(Math.min(5, this.profiles().length)).keys()
        ];
      }
    });
  }

  /**
   * Switches the page of leaderboard that is currently in view.
   * Accomplished by setting shownIndicies to 1-5 or 6-(length of profiles)
   */
  switchPage() {
    if (this.shownIndices.includes(1)) {
      // Generates an array of numbers 5 to length of profile
      this.shownIndices = [
        ...Array(Math.min(5, this.profiles().length - 5)).keys()
      ].map((i) => i + 5);
    } else {
      // At this point we can assume that the array is larger than 5 elements
      this.shownIndices = [...Array(5).keys()];
    }
  }

  /**
   * Gets the class name for the background color of the leaderboard positions
   * @param position position on the leaderboard
   * @returns class name for the background colors
   */
  getBackgroundClass(position: number): string {
    switch (position) {
      case 1:
        return 'primary-fixed-background-leaderboard';
      case 2:
        return 'primary-background';
      case 3:
        return 'primary-fixed-dim-background-leaderboard';

      default:
        return 'secondary-container-background';
    }
  }
}
