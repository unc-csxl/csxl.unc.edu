/**
 * The News Card displays details for events in the paginated list.
 *
 * @author Ajay Gandecha <agandecha@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { ArticleOverview } from '../../welcome.model';

@Component({
  selector: 'news-card',
  templateUrl: './news-card.widget.html',
  styleUrl: './news-card.widget.css'
})
export class NewsCardWidget {
  @Input() article!: ArticleOverview;

  constructor() {}
}
