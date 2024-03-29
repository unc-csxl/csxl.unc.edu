import { Component, Inject, OnDestroy } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Application } from '../admin-application.model';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'application-review-modal',
  templateUrl: './application-review-modal.widget.html',
  styleUrls: ['./application-review-modal.widget.css']
})
export class ApplicationReviewModal {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { application: Application },
    protected http: HttpClient,
    protected snackBar: MatSnackBar
  ) {}

  get applicationProperties(): { key: string; value: any }[] {
    const userData = Object.keys(this.data.application.user).map((key) => ({
      key,
      value: this.data.application.user[key]
    }));

    const applicationData = Object.keys(this.data.application)
      .filter((key) => key !== 'user')
      .map((key) => ({
        key,
        value: this.data.application[key]
      }));

    return [...userData, ...applicationData];
  }

  /** Opens a confirmation snackbar when a checkout is successfully created.
   * @returns {void}
   */
  private onSuccess(application: Application): void {
    this.snackBar.open('Application Reviewed!', '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error creating a checkout.
   * @returns {void}
   */
  private onError(err: any): void {
    console.error('Error: Application Not Reviewed');
    this.snackBar.open('Error: Application Not Reviewed', '', {
      duration: 2000
    });
  }
}
