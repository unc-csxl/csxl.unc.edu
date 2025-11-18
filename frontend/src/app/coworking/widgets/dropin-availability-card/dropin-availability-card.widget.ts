import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges
} from '@angular/core';
import { SeatAvailability } from 'src/app/coworking/coworking.models';

class SeatCategory {
  public title: string;

  public reservable_now: boolean = false;
  public seats_available_now: SeatAvailability[] = [];

  public reservable_soon: boolean = false;
  public next_available?: SeatAvailability;
  public seats_available_soon: SeatAvailability[] = [];

  // TODO: Handle edge case where only openings are < 1hr
  // public truncated: boolean = false;
  // public truncated_at?: Date;

  constructor(title: string) {
    this.title = title;
  }

  push(seat: SeatAvailability) {
    const epsilon = 59 /* seconds */ * 1000; /* milliseconds */
    /* We use an epsilon of ~1 min to combat the potential for clock drift on
           devices relative to the server's time. Difficult to reproduce in dev due
           to server and client sharing the same system clock, but experienced in
           prod on day 0 with many laptops having slightly drifted system clocks. */
    const now = new Date(Date.now() + epsilon);
    const preReservableAt = new Date(
      Date.now() + 10 /*minutes*/ * 60 /*seconds*/ * 1000 /*milliseconds*/
    ); // Currently set by backend/services/coworking/policy.py
    if (seat.availability[0].start <= now) {
      this.seats_available_now.push(seat);
      if (this.seats_available_now.length === 1) {
        this.reservable_now = true;
        this.next_available = seat;
      }
    } else if (seat.availability[0].start <= preReservableAt) {
      this.seats_available_soon.push(seat);
      if (!this.reservable_now && this.seats_available_soon.length === 1) {
        this.reservable_soon = true;
        this.next_available = seat;
      }
    } else {
      // Ignore seats that are not pre-reservable
    }
  }

  availabilityString(): string {
    let result = 'Available ';
    if (this.reservable_now) {
      result += 'now';
    } else if (this.reservable_soon) {
      result += ' in ';
      let now = new Date();
      let start = this.seats_available_soon[0].availability[0].start;
      let delta = Math.ceil((start.getTime() - now.getTime()) / (60 * 1000));
      result += ` ${delta} minutes`;
    } else {
      return 'None available';
    }
    return result;
  }
}

const SITTING_BENCH = 0;
const STANDING_BENCH = 1;
const COLLAB_AREA = 2;

@Component({
  selector: 'coworking-dropin-availability-card',
  templateUrl: './dropin-availability-card.widget.html',
  standalone: false
})
export class CoworkingDropInCard implements OnChanges {
  @Input() seat_availability!: SeatAvailability[];
  @Output() seatsSelected = new EventEmitter<SeatAvailability[]>();

  public categories: SeatCategory[];

  constructor() {
    this.categories = this.initCategories();
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.seat_availability = changes['seat_availability'].currentValue;
    this.categories = this.initCategories();
    for (let seat of this.seat_availability) {
      if (seat.has_monitor) {
        if (seat.sit_stand) {
          this.categories[STANDING_BENCH].push(seat);
        } else {
          this.categories[SITTING_BENCH].push(seat);
        }
      } else {
        this.categories[COLLAB_AREA].push(seat);
      }
    }
  }

  reserve(category: SeatCategory): void {
    this.seatsSelected.emit([
      ...category.seats_available_now,
      ...category.seats_available_soon
    ]);
  }

  private initCategories(): SeatCategory[] {
    return [
      new SeatCategory('Sitting Desk with Monitor'),
      new SeatCategory('Standing Desk with Monitor'),
      new SeatCategory('Communal Area')
    ];
  }
}
