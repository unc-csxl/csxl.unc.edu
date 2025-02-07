/**
 * Simple Widget for the timing spinner on the signage.
 *
 * @input time: time in seconds for one revolution of the widget
 * @output timer_end: event with null data is emitted each time the timer completes
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
  OnDestroy,
  output
} from '@angular/core';
import { Subscription, interval, map } from 'rxjs';

@Component({
  selector: 'page-spinner',
  templateUrl: './page-spinner.widget.html',
  styleUrls: ['./page-spinner.widget.css']
})
export class PageSpinnerWidget implements OnChanges, OnInit, OnDestroy {
  @Input() time!: number;
  timer_end = output<void>();
  timer_subscription!: Subscription;
  time_left = -1;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['time'] && this.time > 0) {
      // Multiplied by 10 so we can have a 10x smoother progress indicator
      this.time_left = this.time * 10;
    }
  }

  ngOnInit(): void {
    this.timer_subscription = interval(100)
      .pipe(
        map(() => {
          if (this.time_left > 0) {
            this.time_left--;
          } else {
            this.timer_end.emit();
            if (this.time) {
              this.time_left = this.time * 10;
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
