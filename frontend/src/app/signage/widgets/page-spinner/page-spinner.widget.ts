/**
 * Simple Widget for the timing spinner on the signage.
 *
 * @input time: time in seconds for one revolution of the widget
 * @input end_action: callback function that is run when the timer ends
 *
 * You can specify a callback function "end_action" that will be run each time the timer ends
 * Make sure to detach this widget when you don't want the end_action to run anymore
 *
 * @author Andrew Lockard
 * @copyright 2024
 * @license MIT
 */
import {
  Component,
  Input,
  OnChanges,
  SimpleChanges,
  OnInit,
  OnDestroy
} from '@angular/core';
import { Subscription, interval, map } from 'rxjs';

@Component({
  selector: 'page-spinner',
  templateUrl: './page-spinner.widget.html',
  styleUrls: ['./page-spinner.widget.css']
})
export class PageSpinnerWidget implements OnChanges, OnInit, OnDestroy {
  @Input() time!: number;
  @Input() end_action: undefined | (() => void) = undefined;
  timer_subscription!: Subscription;
  time_left = -1;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['time'] && this.time > 0) {
      this.time_left = this.time * 100;
    }
  }

  ngOnInit(): void {
    this.timer_subscription = interval(10)
      .pipe(
        map(() => {
          if (this.time_left > 0) {
            this.time_left--;
          } else if (this.time_left == 0) {
            if (this.end_action) {
              this.end_action();
            }
            if (this.time) {
              this.time_left = this.time * 100;
            }
          }
        })
      )
      .subscribe();
  }

  ngOnDestroy(): void {
    if (this.timer_subscription) {
      this.timer_subscription.unsubscribe();
    }
  }
}
