import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'room-dialog',
  template: `
    <div class="dialog-container">
      <button
        class="dialog-close-button"
        mat-icon-button
        (click)="onCloseClick()">
        <mat-icon>close</mat-icon>
      </button>
      <h1 class="dialog-title" mat-dialog-title>Room Information</h1>
      <div class="dialog-content" mat-dialog-content>
        <p>Room: {{ data.id }}</p>
        <p>Capacity: {{ data.capacity }}</p>
        <div *ngIf="data.description">
          <p><strong>Description:</strong></p>
          <p>{{ data.description }}</p>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      .dialog-container {
        position: relative;
        padding: 20px;
        box-sizing: border-box;
        font-family: 'Arial', sans-serif;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      }
      .dialog-close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
        z-index: 1000;
        transform: scale(0.8);
      }
      .dialog-title {
        margin-bottom: 16px;
        font-size: 20px;
      }
      .dialog-content {
        font-size: 16px;
      }

      /* Dark mode styles */
      @media (prefers-color-scheme: dark) {
        .dialog-container {
          color: #fff; /* Light text color for dark mode */
        }
        .dialog-title,
        .dialog-content {
          color: inherit; /* Ensures text elements use the container's color */
        }
      }
    `
  ]
})
export class RoomCapacityDialogComponent {
  constructor(
    private dialogRef: MatDialogRef<RoomCapacityDialogComponent>,
    @Inject(MAT_DIALOG_DATA)
    public data: { id: string; capacity: number; description: string }
  ) {}

  onCloseClick(): void {
    this.dialogRef.close();
  }
}
