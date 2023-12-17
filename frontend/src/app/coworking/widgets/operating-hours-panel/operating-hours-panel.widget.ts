import { Component, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { OperatingHours } from 'src/app/coworking/coworking.models';
import { OperatingHoursDialog } from '../operating-hours-dialog/operating-hours-dialog.widget';

@Component({
  selector: 'coworking-operating-hours-panel',
  templateUrl: './operating-hours-panel.widget.html',
  styleUrls: ['./operating-hours-panel.widget.css']
})
export class CoworkingHoursCard {
  @Input() operatingHours!: OperatingHours[];
  @Input() openOperatingHours?: OperatingHours;

  constructor(public dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(OperatingHoursDialog, {
      data: this.operatingHours
    });
  }
}
