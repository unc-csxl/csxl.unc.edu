import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CoworkingHoursCardDialog } from './coworking-hours-card-dialog/coworking-hours-card-dialog.widget';

@Component({
    selector: 'coworking-hours-card',
    templateUrl: './coworking-hours-card.widget.html',
    styleUrls: ['./coworking-hours-card.widget.css']
})
export class CoworkingHoursCard {

    constructor(public dialog: MatDialog) { }

    openDialog = () => {
        this.dialog.open(CoworkingHoursCardDialog, {
            width: '400px',
        });
    }
}