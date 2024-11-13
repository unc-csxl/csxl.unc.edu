/**
 * The News Card displays details for events in the paginated list.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { ArticleOverview } from '../../../welcome/welcome.model';

@Component({
  selector: 'news-card',
  templateUrl: './news-card.widget.html',
  styleUrl: './news-card.widget.css'
})
export class NewsCardWidget {
  @Input() article!: ArticleOverview;

  constructor() {}
}
