/**
 * Office Hours Widget to Display all currently active office hours, their locations, and queue length
 *
 * @author Andrew Lockard <andrew.lockard15@gmail.com>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { SignageOfficeHours } from '../../signage.model';

@Component({
  selector: 'office-hours-display',
  templateUrl: './office-hours.widget.html',
  styleUrl: './office-hours.widget.css'
})
export class OfficeHoursWidget {
  @Input() officeHours!: SignageOfficeHours[];
}
