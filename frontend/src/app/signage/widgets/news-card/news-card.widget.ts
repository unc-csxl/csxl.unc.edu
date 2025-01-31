/**
 * The News Card displays details for events in the paginated list.
 *
 * @author Will Zahrt <wzahrt@unc.edu>
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ArticleOverview } from '../../../welcome/welcome.model';

@Component({
  selector: 'news-card',
  templateUrl: './news-card.widget.html',
  styleUrl: './news-card.widget.css'
})
export class NewsCardWidget implements OnChanges {
  @Input() articles!: ArticleOverview[];
  shown_article = 0;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['articles']) {
      this.shown_article = 0;
    }
  }

  next_event() {
    this.shown_article = (this.shown_article + 1) % this.articles.length;
  }
}
