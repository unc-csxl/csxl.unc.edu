/**
 * The Occupancy Card displays the current availability of different types of seating in the CSXL.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, effect, input } from '@angular/core';
import { SeatAvailability } from 'src/app/coworking/coworking.models';

interface SeatCategory {
  title: string;
  seats_available_now: number;
}

enum SeatTypes {
  SITTING_MONITOR,
  STANDING_MONITOR,
  COLLAB_SEAT
}

@Component({
    selector: 'occupancy',
    templateUrl: './occupancy.widget.html',
    styleUrls: ['./occupancy.widget.css'],
    standalone: false
})
export class OccupancyWidget {
  /** Inputs and outputs go here */
  seat_availability = input<SeatAvailability[]>([]);

  public categories: SeatCategory[] = [
    {
      title: 'Sitting Desk with Monitor',
      seats_available_now: 0
    },
    {
      title: 'Standing Desk with Monitor',
      seats_available_now: 0
    },
    {
      title: 'Communal Area',
      seats_available_now: 0
    }
  ];

  /** Constructor */
  constructor() {
    effect(() => {
      /**
       * Reset the seat categories and count new seat availability as received
       * from the backend
       *
       * Seats will be regarded as availabile if they are reservable 1 minute from now.
       * This is noted as the epsilon of 59000 milliseconds, and is used to combat
       * clock drift as noted in dropin-availability-card widget in the coworking module
       */
      this.resetCategories();
      const now = new Date(Date.now() + /* epsilon */ 59000 /*milliseconds*/);
      for (let seat of this.seat_availability()) {
        if (seat.availability[0].start <= now) {
          if (seat.has_monitor) {
            if (seat.sit_stand) {
              this.categories[SeatTypes.STANDING_MONITOR].seats_available_now +=
                1;
            } else {
              this.categories[SeatTypes.SITTING_MONITOR].seats_available_now +=
                1;
            }
          } else {
            this.categories[SeatTypes.COLLAB_SEAT].seats_available_now += 1;
          }
        }
      }
    });
  }

  /**
   * Resets the seats_available_now field in each seat category in the categories
   * array to be 0
   */
  private resetCategories() {
    for (let category of this.categories) {
      category.seats_available_now = 0;
    }
  }
}
