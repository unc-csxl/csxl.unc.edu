/**
 * The Roster Component enables instructors to view the roster of their courses.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @author Jade Keegan
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { MatFilterChipFilterLogic } from 'src/app/shared/mat/filter-chip/filter-chip.component';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrl: './statistics.component.css'
})
export class StatisticsComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'statistics',
    title: 'Course',
    component: StatisticsComponent
  };

  filterLogic: MatFilterChipFilterLogic<string> = (item, query) => {
    return item.displayText.toLowerCase().includes(query.toLowerCase());
  };
}
