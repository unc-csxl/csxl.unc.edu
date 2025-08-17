/**
 * The Operating Hours Panel Widget provides quick access to information about
 * the operating hours to users.
 *
 * @author Kris Jordan, Ajay Gandecha, David Foss
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { OperatingHours } from 'src/app/coworking/coworking.models';
import { OperatingHoursDialog } from '../operating-hours-dialog/operating-hours-dialog.widget';
import { Pipe, PipeTransform } from '@angular/core';

@Component({
  selector: 'coworking-operating-hours-panel',
  templateUrl: './operating-hours-panel.widget.html',
  styleUrls: ['./operating-hours-panel.widget.css']
})
export class CoworkingHoursCard {
  @Input() operatingHours!: OperatingHours[];
  @Input() openOperatingHours?: OperatingHours;

  constructor(public dialog: MatDialog) {}

  /** Opens the Operating hours dialog
   *
   * @returns {void}
   */
  openDialog(): void {
    const dialogRef = this.dialog.open(OperatingHoursDialog, {
      autoFocus: false
    });
  }
}

/** Local pipe that capitalizes the first letter of the string. */
@Pipe({
  name: 'operatingHoursCapitalizationPipe'
})
export class OperatingHoursCapitalizationPipe implements PipeTransform {
  transform(sentence: string | null | undefined): string {
    if (!sentence) return '';
    let newSentence = '';
    sentence.split(' ').forEach((segment) => {
      if (segment != 'at') {
        newSentence +=
          segment[0].toUpperCase() + segment.substring(1).toLowerCase();
      } else {
        newSentence += segment;
      }
      newSentence += ' ';
    });
    return newSentence.trimEnd();
  }
}
