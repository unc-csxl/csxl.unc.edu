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
  shownArticle = 0;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['articles']) {
      this.shownArticle = 0;
    }
  }

  nextArticle() {
    this.shownArticle = (this.shownArticle + 1) % this.articles.length;
  }
}
