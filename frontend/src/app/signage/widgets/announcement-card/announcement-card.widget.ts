/**
 * Annoucement Widget to Display Annoucement Headlines on the CSXL Signage
 *
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @license MIT
 * @copyright 2025
 *
 */
import { Component, OnDestroy, input, effect } from '@angular/core';
import { Subscription, timer } from 'rxjs';
import { SignageAnnouncement } from '../../signage.model';

const SECONDS_BETWEEN_CHANGE = 120;

@Component({
  selector: 'announcement-card',
  templateUrl: 'announcement-card.widget.html',
  styleUrls: ['announcement-card.widget.css']
})
export class AnnouncementCardWidget implements OnDestroy {
  announcements = input<SignageAnnouncement[]>([]);
  announcementToDisplay = 0;
  rotatingSubscription: Subscription | null = null;

  constructor() {
    effect(() => {
      /**
       * Setup rotation functionality to support displaying multiple announcements
       * Creates a rotating subscription only if there is more than 1 announcement
       * Uses a timer observable that sets the index announcement to display
       *
       * This is run every time that announcements is changed in case we need to setup/destroy the rotation timer
       */
      this.announcementToDisplay = 0;
      if (
        this.announcements().length > 1 &&
        this.rotatingSubscription == null
      ) {
        this.rotatingSubscription = timer(
          0,
          SECONDS_BETWEEN_CHANGE * 1000
        ).subscribe(() => {
          this.announcementToDisplay =
            (this.announcementToDisplay + 1) % this.announcements().length;
        });
      } else if (
        this.announcements().length <= 1 &&
        this.rotatingSubscription != null
      ) {
        this.rotatingSubscription.unsubscribe();
        this.rotatingSubscription = null;
      }
    });
  }

  ngOnDestroy(): void {
    if (this.rotatingSubscription) {
      this.rotatingSubscription.unsubscribe();
    }
  }
}
