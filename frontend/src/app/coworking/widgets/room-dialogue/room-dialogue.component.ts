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
        <p>Description: {{ data.description }}</p>
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
        background-color: rgb(42, 42, 42);
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
        color: rgb(255, 255, 255);
        font-size: 20px;
      }
      .dialog-content {
        color: rgb(255, 255, 255);
        font-size: 16px;
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
