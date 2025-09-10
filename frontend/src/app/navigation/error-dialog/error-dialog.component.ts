import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
    selector: 'app-error-dialog',
    templateUrl: './error-dialog.component.html',
    styleUrls: [],
    standalone: false
})
export class ErrorDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { message: string }) {}
}
