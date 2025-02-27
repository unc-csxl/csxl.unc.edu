/**
 * Simple Widget for the timing spinner on the signage.
 *
 * @input time: time in seconds for one revolution of the widget
 * @output timerEnd: event with null data is emitted each time the timer completes
 *
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */
import {
  Component,
  input,
  OnInit,
  OnDestroy,
  output,
  effect
} from '@angular/core';
import { Subscription, interval, map } from 'rxjs';

@Component({
  selector: 'page-spinner',
  templateUrl: './page-spinner.widget.html',
  styleUrls: ['./page-spinner.widget.css']
})
export class PageSpinnerWidget implements OnInit, OnDestroy {
  time = input.required<number>();
  timerEnd = output<void>();
  timerSubscription!: Subscription;
  timeLeft = -1;

  constructor() {
    effect(() => {
      /**
       * Resets timeLeft if the time input is changed
       */
      if (this.time() > 0) {
        // Multiplied by 10 so we can have a 10x smoother progress indicator
        this.timeLeft = this.time() * 10;
      }
    });
  }

  ngOnInit(): void {
    this.timerSubscription = interval(100)
      .pipe(
        map(() => {
          if (this.timeLeft > 0) {
            this.timeLeft--;
          } else {
            this.timerEnd.emit();
            if (this.time()) {
              this.timeLeft = this.time() * 10;
            }
          }
        })
      )
      .subscribe();
  }

  ngOnDestroy(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
  }
}
