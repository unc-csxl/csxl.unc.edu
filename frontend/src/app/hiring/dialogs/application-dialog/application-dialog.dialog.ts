/**
 * Enables instructors to view more information about an applicant.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {
  ApplicationReviewOverview,
  ApplicationReviewStatus,
  HiringLevel,
  HiringStatus
} from '../../hiring.models';
import { FormControl } from '@angular/forms';
import { HiringService } from '../../hiring.service';
import { Subscription, debounce, debounceTime, interval, timer } from 'rxjs';

export interface ApplicationDialogData {
  courseSiteId: number;
  review: ApplicationReviewOverview;
  viewOnly?: boolean;
  status?: HiringStatus;
}

@Component({
    selector: 'app-application-dialog',
    templateUrl: './application-dialog.dialog.html',
    styleUrl: './application-dialog.dialog.css',
    standalone: false
})
export class ApplicationDialog implements OnInit, OnDestroy {
  notes = new FormControl('');
  notesSubcription!: Subscription;
  preferredLevel = new FormControl<HiringLevel | undefined>(undefined);
  preferredLevelSubscription!: Subscription;

  constructor(
    protected hiringService: HiringService,
    protected dialogRef: MatDialogRef<ApplicationDialog>,
    @Inject(MAT_DIALOG_DATA) public data: ApplicationDialogData
  ) {
    this.notes.setValue(data.review.notes);
  }

  /** Save the notes data as the user types, with a debounce of 200ms. */
  ngOnInit(): void {
    if (!this.data.viewOnly) {
      this.notesSubcription = this.notesSubcription = this.notes.valueChanges
        .pipe(debounceTime(200))
        .subscribe((_) => {
          this.saveData();
        });
      this.preferredLevel.setValue(this.data.review.level);
      this.preferredLevelSubscription = this.preferredLevel.valueChanges
        .subscribe((_) => {
          this.saveData();
        });
    }
  }

  /** Unsubsribe from the notes subscription when the page is closed. */
  ngOnDestroy(): void {
    this.notesSubcription.unsubscribe();
    this.preferredLevelSubscription.unsubscribe();
  }

  youtubeVideoId(): string | undefined {
    let splitUrl = this.data.review.application.intro_video_url?.split('?v=');
    return splitUrl?.length ?? 0 > 0 ? splitUrl![1] : undefined;
  }

  saveData() {
    // Replace the current review based on its place in the hiring status.
    if (this.data.review.status == ApplicationReviewStatus.NOT_PREFERRED) {
      this.data.status!.not_preferred[this.data.review.preference].notes =
        this.notes.value ?? '';
      this.data.status!.not_preferred[this.data.review.preference].level =
        this.preferredLevel.value ?? null;
    }
    if (this.data.review.status == ApplicationReviewStatus.NOT_PROCESSED) {
      this.data.status!.not_processed[this.data.review.preference].notes =
        this.notes.value ?? '';
      this.data.status!.not_processed[this.data.review.preference].level =
        this.preferredLevel.value ?? null;
    }
    if (this.data.review.status == ApplicationReviewStatus.PREFERRED) {
      this.data.status!.preferred[this.data.review.preference].notes =
        this.notes.value ?? '';
      this.data.status!.preferred[this.data.review.preference].level =
        this.preferredLevel.value ?? null;
    }

    // Persist the data
    this.hiringService
      .updateStatus(this.data.courseSiteId, this.data.status!)
      .subscribe((hiringStatus) => {
        this.data.status = hiringStatus;
      });
  }
}
