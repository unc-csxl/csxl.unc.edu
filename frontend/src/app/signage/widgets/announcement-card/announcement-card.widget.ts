/**
 * Annoucement Widget to Display Annoucement Headlines on the CSXL Signage
 *
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @license MIT
 * @copyright 2025
 *
 */
import {
  Component,
  Input,
  OnChanges,
  SimpleChanges,
  OnDestroy
} from '@angular/core';
import { Subscription, timer } from 'rxjs';

const SECONDS_BETWEEN_CHANGE = 120;

@Component({
  selector: 'announcement-card',
  templateUrl: 'announcement-card.widget.html',
  styleUrls: ['announcement-card.widget.css']
})
export class AnnouncementCardWidget implements OnChanges, OnDestroy {
  @Input() announcements!: string[];
  announcementToDisplay = 0;
  rotatingSubscription: Subscription | null = null;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['announcements']) {
      this.announcementToDisplay = 0;
      // Handle rotating between multiple announcements
      if (this.announcements.length > 1 && this.rotatingSubscription == null) {
        this.rotatingSubscription = timer(
          0,
          SECONDS_BETWEEN_CHANGE * 1000
        ).subscribe(() => {
          this.announcementToDisplay =
            (this.announcementToDisplay + 1) % this.announcements.length;
        });
      } else if (
        this.announcements.length <= 1 &&
        this.rotatingSubscription != null
      ) {
        this.rotatingSubscription.unsubscribe();
        this.rotatingSubscription = null;
      }
    }
  }

  ngOnDestroy(): void {
    if (this.rotatingSubscription) {
      this.rotatingSubscription.unsubscribe();
    }
  }
}
