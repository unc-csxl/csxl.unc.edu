import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
    selector: 'coworking-hours-dialog',
    templateUrl: './coworking-hours-card-dialog.widget.html',
    styleUrls: ['./coworking-hours-card-dialog.widget.css']
})
export class CoworkingHoursCardDialog {

    constructor(public dialogRef: MatDialogRef<CoworkingHoursCardDialog>) { }
}