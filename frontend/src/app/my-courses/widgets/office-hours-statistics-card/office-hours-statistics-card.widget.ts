/**
 * Widget to display information about office hours statistics.
 *
 * @author Ajay Gandecha <ajay@cs.unc.edu>
 * @license MIT
 * @copyright 2025
 */

import { Component, input } from '@angular/core';

@Component({
    selector: 'office-hours-statistics-card',
    templateUrl: './office-hours-statistics-card.widget.html',
    styleUrl: './office-hours-statistics-card.widget.css',
    standalone: false
})
export class OfficeHoursStatisticsCardWidget {
  title = input<string>('');
  leftStatistic = input<string>('');
  leftStatisticLabel = input<string>('');
  rightStatistic = input<string | undefined>(undefined);
  rightStatisticLabel = input<string | undefined>(undefined);
}
